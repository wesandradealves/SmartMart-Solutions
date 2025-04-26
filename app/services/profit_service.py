from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import models
from app.utils.profit import calculate_profit

def calculate_total_profit(db: Session, days: int = 365) -> float:
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    sales = db.query(models.Sale).filter(models.Sale.date >= cutoff_date).all()

    total_profit = sum(calculate_profit(sale).profit for sale in sales)

    return total_profit
