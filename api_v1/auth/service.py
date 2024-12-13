from datetime import datetime, timedelta

import jwt
import aiosqlite

from fastapi import (
    HTTPException,
    status,
    Security,
)
from sqlalchemy import select
from fastapi.security import APIKeyHeader

from api_v1.db.crud import async_create_db
from api_v1.db.models.models import Token
from api_v1.db.session import async_session_factory
from core.config import settings


token_header_auth = APIKeyHeader(
    name="Authorization",
    description="Token для работы с API",
    scheme_name="APIKeyHeader",
    auto_error=False,
)

SECRET_KEY = settings.auth.JWT_SECRET
ALGORITHM = settings.auth.JWT_ALG
ACCESS_TOKEN_EXPIRE_DAYS = settings.auth.JWT_EXP


async def is_valid_jwt(token):
    try:
        # Decode the token to get the payload
        decoded_token = jwt.decode(
            token, algorithms=[ALGORITHM], options={"verify_signature": False}
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def is_valid_token(token: str = Security(token_header_auth)):
    # Check if token is not empty
    if not token or not await check_token_to_db(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Token",
        )

    # Check if token is valid
    if not await is_valid_jwt(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Token, not a valid JWT",
        )

    # Check if token is a string
    if not isinstance(token, str):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Token! It should be of type 'str', not '{type(token).__name__}'.",
        )

    # Check if token contains spaces
    if " " in token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Token! It should not contain spaces.",
        )

    return token


async def create_access_token(data: dict, expires_delta: timedelta = None):
    # Create access token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def save_token_to_db(email: str, token: str, session):
    await async_create_db()
    email = email.lower()

    # Создаем запрос для выборки токена по email
    statement = select(Token).where(
        Token.email == email
    )  # Создаем оператор для выборки

    # Выполняем запрос и получаем результат
    result = await session.execute(statement)  # Передаем statement в execute

    # Извлекаем первую запись из результата
    token_entry = result.scalars().first()

    if token_entry:
        # Если запись существует, обновляем токен
        token_entry.token = token
    else:
        # Если записи нет, создаем новую
        new_token = Token(email=email, token=token)
        session.add(new_token)
    await session.commit()


async def check_token_to_db(token: str) -> bool:
    # Выполняем запрос для проверки наличия токена
    async with async_session_factory() as session:
        result = await session.execute(select(Token).filter_by(token=token))
        token_entry = result.scalars().first()
        return token_entry is not None


async def get_token_from_db(email: str, session):
    # Выполняем запрос для получения токена по email
    result = await session.execute(select(Token).filter_by(email=email.lower()))
    token_entry = result.scalars().first()
    return token_entry.token if token_entry else None
