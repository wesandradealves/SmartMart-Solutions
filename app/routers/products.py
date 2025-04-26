from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models
from app.schemas import schemas
from app.services import csv_importer
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.post("", response_model=schemas.Product)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    normalized_name = product.name.strip().lower()

    existing_product = db.query(models.Product).filter(
        models.Product.name.ilike(normalized_name)
    ).first()

    if existing_product:
        raise HTTPException(status_code=400, detail="Produto com o mesmo nome já existe")

    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, updated_product: schemas.ProductBase, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    normalized_name = updated_product.name.strip().lower()

    existing_product = db.query(models.Product).filter(
        models.Product.id != product_id,  # ignora ele mesmo
        models.Product.name.ilike(normalized_name)
    ).first()

    if existing_product:
        raise HTTPException(status_code=400, detail="Já existe outro produto com esse nome")

    for key, value in updated_product.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(product)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}

@router.post("/upload-csv")
def upload_csv(file: UploadFile, db: Session = Depends(get_db)):
    return csv_importer.import_products_csv(file, db)
