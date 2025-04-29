# remove_orphan_sales.py

from app.database import SessionLocal
from app.models import models

def remove_orphan_sales():
    db = SessionLocal()
    try:
        valid_product_ids = set(pid for (pid,) in db.query(models.Product.id).all())
        orphan_sales = db.query(models.Sale).filter(~models.Sale.product_id.in_(valid_product_ids)).all()
        print(f"Encontradas {len(orphan_sales)} vendas órfãs.")
        for sale in orphan_sales:
            print(f"Removendo venda id={sale.id} (product_id={sale.product_id})")
            db.delete(sale)
        db.commit()
        print("Vendas órfãs removidas com sucesso.")
    finally:
        db.close()

if __name__ == "__main__":
    remove_orphan_sales()