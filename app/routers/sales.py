from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models import models
from app.schemas import schemas
from app.utils.profit import calculate_profit
from app.services.profit_service import calculate_total_profit
from app.database import get_db
from app.utils.pagination import paginate
from app.schemas.schemas import PaginatedResponse
from datetime import datetime, timedelta

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("", response_model=PaginatedResponse[schemas.SaleWithProfit])
def get_sales(
    db: Session = Depends(get_db),
    sort_by: str = Query("total_price", enum=["total_price", "profit", "date"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    days: int = Query(365, ge=1, description="Número de dias para considerar (padrão: últimos 365 dias)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    sales = db.query(models.Sale).filter(models.Sale.date >= cutoff_date).all()

    sales_with_profit = [calculate_profit(sale) for sale in sales]

    if sort_by == "profit":
        sales_with_profit.sort(key=lambda x: x.profit, reverse=(sort_order == "desc"))
    elif sort_by == "date":
        sales_with_profit.sort(key=lambda x: x.date, reverse=(sort_order == "desc"))
    else:
        sales_with_profit.sort(key=lambda x: x.total_price, reverse=(sort_order == "desc"))

    total = len(sales_with_profit)
    items = sales_with_profit[skip:skip+limit]

    return PaginatedResponse(
        items=items,
        total=total
    )
    
@router.get("/profit/total")
def get_total_profit(
    db: Session = Depends(get_db),
    days: int = Query(365, ge=1, description="Número de dias para considerar (padrão: últimos 365 dias)"),
    product_id: int = Query(None, description="ID do produto para filtrar as vendas")
):
    result = calculate_total_profit(db, days, product_id)
    return result


@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.put("/{sale_id}", response_model=schemas.Sale)
def update_sale(sale_id: int, updated_sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    for key, value in updated_sale.dict().items():
        setattr(sale, key, value)

    db.commit()
    db.refresh(sale)
    return sale

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    db.delete(sale)
    db.commit()
    return {"detail": "Venda deletada com sucesso"}
