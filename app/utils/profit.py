from app.schemas.schemas import Sale

# def calculate_profit(sales):
#     sales_with_profit = []
#     for s in sales:
#         sale_dict = s.__dict__ 
#         sale_dict['profit'] = s.total_price 
#         sales_with_profit.append(sale_dict)  
#     return sales_with_profit

def calculate_profit(sale):
    sale_dict = sale.__dict__ 
    sale_dict['profit'] = sale.total_price  
    return sale_dict