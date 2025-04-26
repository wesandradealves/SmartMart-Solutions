import pandas as pd
from app.database import SessionLocal, create_tables
from app.models import models
from app.services import security 

create_tables()

db_session = SessionLocal()

# Categories
categories = pd.read_csv("data/categories.csv")
for _, row in categories.iterrows():
    db_session.add(models.Category(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        price=row["price"],
        brand=row["brand"]
    ))

# Products
products = pd.read_csv("data/products.csv")
for _, row in products.iterrows():
    db_session.add(models.Product(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        price=row["price"],
        category_id=row["category_id"],
        brand=row["brand"]
    ))

# Sales
sales = pd.read_csv("data/sales.csv")
sales['date'] = pd.to_datetime(sales['date'])
for _, row in sales.iterrows():
    db_session.add(models.Sale(
        product_id=row["product_id"],
        quantity=row["quantity"],
        total_price=row["total_price"],
        date=row["date"]
    ))

# Users
users = pd.read_csv("data/users.csv")
users['created_at'] = pd.to_datetime(users['created_at'])
for _, row in users.iterrows():
    db_session.add(models.User(
        id=row["id"],
        email=row["email"],
        username=row["username"],
        password=security.hash_password(row["password"]), 
        role=row["role"],
        created_at=row["created_at"]
    ))

db_session.commit()
db_session.close()

print("✅ Dados populados com sucesso.")
