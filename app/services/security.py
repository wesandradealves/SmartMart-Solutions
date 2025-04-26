from passlib.context import CryptContext
import os
from fastapi import HTTPException
from itsdangerous import URLSafeTimedSerializer
from app.models import models

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
serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_session_token(user: models.User) -> str:
    """
    Cria um token de sessão para um usuário autenticado.
    :param user: O objeto do usuário autenticado.
    :return: Token de sessão.
    """
    return serializer.dumps({"user_id": user.id, "email": user.email, "role": user.role.name})

def verify_session_token(token: str, expiration: int = 3600) -> dict:
    """
    Verifica a validade de um token de sessão e retorna os dados decodificados.
    :param token: O token de sessão a ser verificado.
    :param expiration: Tempo de expiração do token em segundos (padrão é 3600 segundos ou 1 hora).
    :return: Dados decodificados do token.
    :raises HTTPException: Se o token for inválido ou expirado.
    """
    try:
        data = serializer.loads(token, max_age=expiration)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return data
