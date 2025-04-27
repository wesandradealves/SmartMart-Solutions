from passlib.context import CryptContext
import os
from fastapi import HTTPException
from app.models import models
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Gera o hash de uma senha usando bcrypt.
    :param password: Senha em texto simples.
    :return: Senha hasheada.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash.
    :param plain_password: Senha em texto simples fornecida pelo usuário.
    :param hashed_password: Senha hasheada armazenada no banco de dados.
    :return: True se a senha corresponder, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"

def create_session_token(user: models.User) -> str:
    # Cria um JWT para sessão
    payload = {"user_id": user.id, "email": user.email, "role": user.role.name}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_session_token(token: str) -> dict:
    # Verifica o JWT e retorna o payload
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return data
