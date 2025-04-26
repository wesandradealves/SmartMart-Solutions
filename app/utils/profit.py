from app.schemas.schemas import Sale

def calculate_profit(sale):
    sale_dict = sale.__dict__ 
    sale_dict['profit'] = sale.total_price  
    return sale_dict