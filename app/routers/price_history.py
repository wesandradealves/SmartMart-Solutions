from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app.models import models
from app.schemas import schemas
from typing import List

router = APIRouter(prefix="/price-history", tags=["price-history"])

@router.get("/{product_id}", response_model=List[schemas.PriceHistory])
def get_price_history(
    product_id: int,
    db: Session = Depends(get_db),
    sort: str = Query("asc", enum=["asc", "desc"]),
    sort_by: str = Query("date", enum=["date", "price"])
):
    query = db.query(models.PriceHistory).filter(models.PriceHistory.product_id == product_id)

    sort_column_map = {
        "date": models.PriceHistory.date,
        "price": models.PriceHistory.price
    }

    sort_column = sort_column_map.get(sort_by, models.PriceHistory.date)

    query = query.order_by(desc(sort_column) if sort == "desc" else asc(sort_column))

    price_history = query.all()
    
    if not price_history:
        raise HTTPException(status_code=404, detail="Histórico de preços não encontrado para o produto")
    
    return price_history
