import pandas as pd
from app.models import models
from app.services.security import hash_password
from datetime import datetime

def import_products_csv(file, db):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        product = models.Product(
            name=row["name"],
            description=row.get("description"),  
            price=row["price"],
            category_id=row["category_id"],
            brand=row.get("brand") 
        )
        db.add(product)
    db.commit()
    return {"message": "Produtos importados com sucesso."}

def import_users_csv(file, db):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        user = models.User(
            email=row["email"].strip().lower(),
            username=row["username"].strip(),
            password=hash_password(row["password"].strip()) if "password" in row and pd.notna(row["password"]) else hash_password(row["username"].strip()),  
            role=row["role"].strip()
        )
        db.add(user)
    db.commit()
    return {"message": "Usuários importados com sucesso."}

def import_categories_csv(file, db):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        category = models.Category(
            name=row["name"].strip(),
            description=row.get("description", "").strip() if pd.notna(row.get("description")) else None
        )
        db.add(category)
    db.commit()
    return {"message": "Categorias importadas com sucesso."}

def import_sales_csv(file, db):
    try:
        df = pd.read_csv(file.file)
        for _, row in df.iterrows():
            sale = models.Sale(
                product_id=row["product_id"],
                quantity=row["quantity"],
                total_price=row["total_price"],
                date=datetime.strptime(str(row["date"]), "%Y-%m-%d %H:%M:%S")
            )
            db.add(sale)
        db.commit()
        return {"message": "Vendas importadas com sucesso."}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}