from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models
from app.schemas import schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("", response_model=list[schemas.Category])
# def get_categories(db: Session = Depends(get_db)):
#     return db.query(models.Category).all()

@router.get("", response_model=list[schemas.Category])
def get_categories(
    db: Session = Depends(get_db),
    sort_by: str = "name",  
    sort_order: str = "asc"  
):
    if sort_order == "desc":
        sort_direction = desc
    else:
        sort_direction = asc

    if sort_by == "id":
        categories = db.query(models.Category).order_by(sort_direction(models.Category.id)).all()
    else:
        categories = db.query(models.Category).order_by(sort_direction(models.Category.name)).all()

    return categories

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    normalized_name = category.name.strip().lower()

    existing_category = db.query(models.Category).filter(
        models.Category.name.ilike(normalized_name)
    ).first()

    if existing_category:
        raise HTTPException(status_code=400, detail="Categoria com o mesmo nome já existe")

    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, updated_category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    normalized_name = updated_category.name.strip().lower()

    existing_category = db.query(models.Category).filter(
        models.Category.id != category_id, 
        models.Category.name.ilike(normalized_name)
    ).first()

    if existing_category:
        raise HTTPException(status_code=400, detail="Já existe outra categoria com esse nome")

    for key, value in updated_category.dict().items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(category)
    db.commit()
    return {"detail": "Categoria deletada com sucesso"}
