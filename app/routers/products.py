from fastapi import APIRouter, Depends, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from app.models import models
from app.schemas import schemas
from app.services import csv_importer
from app.database import get_db
from app.utils.pagination import paginate

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.Product])
def get_products(
    db: Session = Depends(get_db),
    category_id: int = Query(None),
    title: str = Query(None),
    sort: str = Query("asc", enum=["asc", "desc"]),
    sort_by: str = Query("name", enum=["id", "name", "category_id", "brand", "price"]),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    query = db.query(models.Product).options(joinedload(models.Product.category))

    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    if title:
        query = query.filter(models.Product.name.ilike(f"%{title}%"))

    sort_column_map = {
        "id": models.Product.id,
        "name": models.Product.name,
        "category_id": models.Product.category_id,
        "brand": models.Product.brand,
        "price": models.Product.price
    }
    sort_column = sort_column_map.get(sort_by, models.Product.name)
    query = query.order_by(desc(sort_column) if sort == "desc" else asc(sort_column))

    products, total = paginate(query, skip, limit)

    return schemas.PaginatedResponse(
        items=products,
        total=total
    )


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
def update_product(
    product_id: int,
    updated_product: schemas.ProductUpdate,  
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if updated_product.name is not None:
        normalized_name = updated_product.name.strip().lower()
        existing_product = db.query(models.Product).filter(
            models.Product.id != product_id, 
            models.Product.name.ilike(normalized_name)
        ).first()

        if existing_product:
            raise HTTPException(status_code=400, detail="Já existe outro produto com esse nome")

        product.name = updated_product.name.strip()

    if updated_product.description is not None:
        product.description = updated_product.description

    if updated_product.price is not None:
        product.price = updated_product.price

    if updated_product.category_id is not None:
        product.category_id = updated_product.category_id

    if updated_product.brand is not None:
        product.brand = updated_product.brand.strip()

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

@router.put("/categories/{category_id}/discount")
def update_category_discount(
    category_id: int,
    discount_percentage: float = Query(..., ge=0, le=100), 
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    category.discount_percentage = discount_percentage

    update_product_prices(db, category_id)

    products = db.query(models.Product).filter(models.Product.category_id == category_id).all()

    db.commit()

    return {
        "success": True,
        "message": "Desconto atualizado com sucesso",
        "discount_percentage": discount_percentage,
        "category_id": category_id,
        "updated_products": [
            {
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "category_id": product.category_id
            }
            for product in products
        ]
    }

def update_product_prices(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        return None

    products = db.query(models.Product).filter(models.Product.category_id == category_id).all()

    for product in products:
        discount_amount = product.price * (category.discount_percentage / 100)
        new_price = product.price - discount_amount
        if new_price < 0:
            new_price = 0 

        product.price = new_price

        add_price_history(db, product.id, new_price)

    db.commit()


def add_price_history(db: Session, product_id: int, new_price: float, reason: str = None):
    price_history = models.PriceHistory(
        product_id=product_id,
        price=new_price,
        reason=reason
    )
    db.add(price_history)
    db.commit()
    db.refresh(price_history)
    return price_history