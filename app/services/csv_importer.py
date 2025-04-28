import pandas as pd
from app.models import models

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