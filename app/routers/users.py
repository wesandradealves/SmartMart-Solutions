from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Cookie, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.services import security
from app.utils.pagination import paginate
from app.schemas.schemas import PaginatedResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    normalized_email = user.email.strip().lower()

    existing_user = db.query(models.User).filter(models.User.email == normalized_email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário com o mesmo e-mail já existe")

    db_user = models.User(
        email=user.email,
        username=user.username,
        password=security.hash_password(user.password),  
        role=user.role,
        created_at=user.created_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("", response_model=PaginatedResponse[schemas.User])
def get_users(
    db: Session = Depends(get_db),
    sort: str = Query("asc", enum=["asc", "desc"]),
    sort_by: str = Query("username", enum=["username", "email", "role", "created_at"]),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    query = db.query(models.User)

    sort_column_map = {
        "username": models.User.username,
        "email": models.User.email,
        "role": models.User.role,
        "created_at": models.User.created_at
    }

    sort_column = sort_column_map.get(sort_by, models.User.username)

    query = query.order_by(desc(sort_column) if sort == "desc" else asc(sort_column))

    users, total = paginate(query, skip, limit)

    for user in users:
        user.hashed_password = user.password  
        delattr(user, 'password') 

    return PaginatedResponse(items=users, total=total)

@router.put("/{user_id}")
def update_user(user_id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if updated_user.email is not None:
        normalized_email = updated_user.email.strip().lower()
        updated_user.email = normalized_email

    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    response = JSONResponse(content={"message": "Dados alterados com sucesso", "uid": user_id})
    return response

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()
    response = JSONResponse(content={"message": "Usuário deletado com sucesso", "uid": user_id})
    return response

@router.post("/login")
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    print(f"Login attempt: email={user.email}, username={user.username}")  # Log para depuração
    db_user = None

    if user.email:
        normalized_email = user.email.strip().lower()
        db_user = db.query(models.User).filter(models.User.email == normalized_email).first()
    elif user.username:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = security.create_session_token(db_user)
    response_message = f"✅ Você está logado como {db_user.username}"

    response = JSONResponse(content={"message": response_message, "token": token})
    response.set_cookie(key="session_token", value=token, httponly=True, max_age=3600)

    return response

@router.post("/logout")
def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=400, detail="Nenhuma sessão ativa")

    try:
        security.verify_session_token(session_token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    # Deleta o cookie de sessão
    response.delete_cookie("session_token", path="/")
    return {"message": "Logout bem-sucedido"}