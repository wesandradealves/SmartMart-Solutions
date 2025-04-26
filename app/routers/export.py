from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io

from app.database import get_db
from app import models

router = APIRouter(prefix="/export", tags=["Export"])

def generate_csv(data, headers):
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(headers)
    for item in data:
        writer.writerow([getattr(item, h) for h in headers])
    stream.seek(0)
    return stream

@router.get("/products")
def export_products_csv(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    headers = ["id", "name", "description", "price", "category_id", "brand"]
    return StreamingResponse(generate_csv(products, headers), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=products.csv"})

@router.get("/sales")
def export_sales_csv(db: Session = Depends(get_db)):
    sales = db.query(models.Sale).all()
    headers = ["id", "product_id", "quantity", "total_price", "date"]
    return StreamingResponse(generate_csv(sales, headers), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sales.csv"})

@router.get("/categories")
def export_categories_csv(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    headers = ["id", "name", "description", "price", "brand"]
    return StreamingResponse(generate_csv(categories, headers), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=categories.csv"})

@router.get("/sales_with_profit")
def export_sales_with_profit_csv(db: Session = Depends(get_db)):
    sales = db.query(models.Sale).all()
    headers = ["id", "product_id", "quantity", "total_price", "date", "profit"]
    return StreamingResponse(generate_csv(sales, headers), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sales_with_profit.csv"})