# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from app.models import models
# from app.utils.profit import calculate_profit

# def calculate_total_profit(db: Session, days: int = 365, product_id: int = None) -> dict:
#     cutoff_date = datetime.utcnow() - timedelta(days=days)
    
#     sales_query = db.query(models.Sale).filter(models.Sale.date >= cutoff_date)
    
#     if product_id:
#         sales_query = sales_query.filter(models.Sale.product_id == product_id)
    
#     sales = sales_query.all()

#     total_profit = sum(calculate_profit(sale).profit for sale in sales)

#     return {
#         "total_profit": total_profit,
#         "days": days,
#         "sales": [
#             {
#                 "product_id": sale.product_id,
#                 "quantity": sale.quantity,
#                 "total_price": sale.total_price,
#                 "date": sale.date,
#                 "profit": calculate_profit(sale).profit
#             }
#             for sale in sales
#         ]
#     }

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import models
from app.utils.profit import calculate_profit

def calculate_total_profit(db: Session, days: int = 365, product_id: int = None) -> dict:
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    sales_query = db.query(models.Sale).filter(models.Sale.date >= cutoff_date)
    
    if product_id:
        sales_query = sales_query.filter(models.Sale.product_id == product_id)
    
    sales = sales_query.all()

    total_profit = sum(calculate_profit(sale).profit for sale in sales)
    
    product_name = None
    if product_id:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if product:
            product_name = product.name

    return {
        "total_profit": total_profit,
        "days": days,
        "name": product_name,  
        "sales": [
            {
                "product_id": sale.product_id,
                "quantity": sale.quantity,
                "total_price": sale.total_price,
                "date": sale.date,
                "profit": calculate_profit(sale).profit
            }
            for sale in sales
        ]
    }
