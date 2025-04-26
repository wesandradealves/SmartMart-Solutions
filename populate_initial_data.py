import pandas as pd
from app.database import SessionLocal, create_tables
from app.models import models

# Criação das tabelas
create_tables()

# Criação de sessão para inserção de dados
db_session = SessionLocal()

# Leitura e inserção dos dados de categorias
categories = pd.read_csv("data/categories.csv")
for _, row in categories.iterrows():
    db_session.add(models.Category(id=row["id"], name=row["name"], description=row["description"], price=row["price"], brand=row["brand"]))

# Leitura e inserção dos dados de produtos
products = pd.read_csv("data/products.csv")
for _, row in products.iterrows():
    db_session.add(models.Product(id=row["id"], name=row["name"], description=row["description"], price=row["price"], category_id=row["category_id"], brand=row["brand"]))

# Leitura e inserção dos dados de vendas
sales = pd.read_csv("data/sales.csv")
sales['date'] = pd.to_datetime(sales['date'])  # Conversão para datetime
for _, row in sales.iterrows():
    db_session.add(models.Sale(product_id=row["product_id"], quantity=row["quantity"], total_price=row["total_price"], date=row["date"]))

# Commit para salvar os dados
db_session.commit()
db_session.close()

print("✅ Dados populados com sucesso.")
