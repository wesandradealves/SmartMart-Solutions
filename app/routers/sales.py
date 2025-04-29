from fastapi import APIRouter, Depends, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.utils.pagination import paginate
from app.services.csv_importer import import_sales_csv
from fastapi.responses import StreamingResponse
import csv
import io

router = APIRouter(prefix="/sales", tags=["sales"])

def generate_csv(data, headers):
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(headers)
    for item in data:
        writer.writerow([getattr(item, h) for h in headers])
    stream.seek(0)
    return stream

@router.get("", response_model=schemas.PaginatedResponse[schemas.SaleWithProductName])
def get_sales(
    db: Session = Depends(get_db),
    page: int = 1,
    sort_by: str = Query("date", enum=["id", "product_id", "quantity", "total_price", "date"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    product_id: int = Query(None)
):
    if sort_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort_order. Must be 'asc' or 'desc'.")
    print(f"Query parameters received: sort_by={sort_by}, sort_order={sort_order}, page={page}, skip={skip}, limit={limit}, product_id={product_id}")
    query = db.query(models.Sale)
    if product_id is not None:
        query = query.filter(models.Sale.product_id == product_id)
    sort_column_map = {
        "id": models.Sale.id,
        "product_id": models.Sale.product_id,
        "quantity": models.Sale.quantity,
        "total_price": models.Sale.total_price,
        "date": models.Sale.date
    }
    sort_column = sort_column_map.get(sort_by, models.Sale.date)
    query = query.order_by(desc(sort_column) if sort_order == "desc" else asc(sort_column))
    sales, total = paginate(query, skip, limit)
    product_ids = [sale.product_id for sale in sales]
    products = db.query(models.Product.id, models.Product.name).filter(models.Product.id.in_(product_ids)).all()
    product_map = {pid: name for pid, name in products}
    sales_with_name = [
        schemas.SaleWithProductName(**sale.__dict__, product_name=product_map.get(sale.product_id, str(sale.product_id)))
        for sale in sales
    ]
    return schemas.PaginatedResponse(
        items=sales_with_name,
        total=total
    )

@router.post("", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.put("/{sale_id}")
def update_sale(
    sale_id: int,
    updated_sale: schemas.SaleUpdate,
    db: Session = Depends(get_db)
):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    for key, value in updated_sale.dict(exclude_unset=True).items():
        setattr(sale, key, value)

    db.commit()
    db.refresh(sale)
    return {"message": "Venda atualizada com sucesso", "sale": sale}

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    db.delete(sale)
    db.commit()
    return {"detail": "Venda deletada com sucesso"}

@router.post("/upload-csv")
def upload_sales_csv(file: UploadFile, db: Session = Depends(get_db)):
    return import_sales_csv(file, db)

@router.get("/export")
def export_sales_csv(db: Session = Depends(get_db)):
    sales = db.query(models.Sale).all()
    headers = ["id", "product_id", "quantity", "total_price", "date"]
    return StreamingResponse(
        generate_csv(sales, headers),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sales.csv"}
    )
