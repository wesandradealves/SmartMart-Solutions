from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, aliased
from sqlalchemy import asc, desc, func
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.utils.pagination import paginate
from app.schemas.schemas import PaginatedResponse

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.Category])
def get_categories(
    db: Session = Depends(get_db),
    sort_by: str = Query("name", enum=["id", "name"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    sort_direction = desc if sort_order == "desc" else asc
    sort_column = models.Category.id if sort_by == "id" else models.Category.name

    query = db.query(models.Category).order_by(sort_direction(sort_column))

    query = query.outerjoin(models.Product).group_by(models.Category.id)

    categories, total = paginate(query, skip, limit)

    for category in categories:
        category_data = db.query(models.Product).filter(models.Product.category_id == category.id).count()
        category.total_products = category_data
        category.description = category.description or ""

    return schemas.PaginatedResponse(
        items=categories,
        total=total
    )


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    normalized_name = category.name.strip().lower()

    existing_category = db.query(models.Category).filter(
        models.Category.name.ilike(normalized_name)
    ).first()

    if existing_category:
        raise HTTPException(status_code=400, detail="Categoria com o mesmo nome já existe")

    if category.discount_percentage is not None and (category.discount_percentage < 0 or category.discount_percentage > 100):
        raise HTTPException(status_code=400, detail="O campo 'discount_percentage' deve estar entre 0 e 100")

    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    updated_category: schemas.CategoryCreate = None,
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    if not updated_category:
        raise HTTPException(status_code=400, detail="Nenhum dado foi fornecido para atualização.")

    if updated_category.name:
        normalized_name = updated_category.name.strip().lower()
        existing_category = db.query(models.Category).filter(
            models.Category.id != category_id, 
            models.Category.name.ilike(normalized_name)
        ).first()
        
        if existing_category:
            raise HTTPException(status_code=400, detail="Já existe outra categoria com esse nome")

        category.name = updated_category.name.strip()

    if updated_category.description is not None:
        category.description = updated_category.description

    if updated_category.discount_percentage is not None:
        category.discount_percentage = updated_category.discount_percentage

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
