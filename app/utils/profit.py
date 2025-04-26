from app.schemas.schemas import Sale
from app.schemas import schemas

def calculate_profit(sale):
    profit = sale.total_price * 0.2  
    sale_with_profit = schemas.SaleWithProfit(
        id=sale.id,
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_price=sale.total_price,
        date=sale.date,
        profit=profit
    )
    return sale_with_profit
