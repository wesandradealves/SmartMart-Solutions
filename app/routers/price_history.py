from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/price-history", tags=["price-history"])

@router.get("/{product_id}", response_model=schemas.PriceHistory)
def get_price_history(product_id: int, db: Session = Depends(get_db)):
    price_history = db.query(models.PriceHistory).filter(models.PriceHistory.product_id == product_id).all()
    if not price_history:
        raise HTTPException(status_code=404, detail="Histórico de preços não encontrado para o produto")
    return price_history
