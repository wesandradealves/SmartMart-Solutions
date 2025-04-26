from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models
from app.schemas import schemas
from app.utils.profit import calculate_profit
from app.database import get_db

router = APIRouter(prefix="/sales", tags=["sales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.SaleWithProfit])
def get_sales(
    db: Session = Depends(get_db),
    sort_by: str = "total_price",  
    sort_order: str = "asc" 
):
    if sort_order == "desc":
        sort_direction = desc
    else:
        sort_direction = asc

    sales = db.query(models.Sale).all()

    sales_with_profit = [calculate_profit(sale) for sale in sales]

    if sort_by == "profit":
        sales_with_profit.sort(key=lambda x: x.profit, reverse=(sort_order == "desc"))
    elif sort_by == "total_price":
        sales_with_profit.sort(key=lambda x: x.total_price, reverse=(sort_order == "desc"))

    return sales_with_profit

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
