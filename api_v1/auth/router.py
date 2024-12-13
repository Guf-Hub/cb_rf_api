from datetime import timedelta
from typing import Annotated, Union

from fastapi import (
    APIRouter,
    Query,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TokenModel, TokenRequestModel
from .service import (
    check_token_to_db,
    get_token_from_db,
    create_access_token,
    save_token_to_db,
    ACCESS_TOKEN_EXPIRE_DAYS,
)
from core.dependencies import TokenDep
from api_v1.db.session import SessionDep

router = APIRouter(tags=["Auth"])


# @router.get("/login", summary="Авторизация")
# async def login():
#     return {"message": "Login successful"}


@router.get(
    "/get",
    summary="Получить токен",
    response_model=TokenModel,
)
async def get_token(
    query: Annotated[
        Union[TokenRequestModel],
        Query(
            title="Email пользователя",
            description="Введите действительный адрес электронной почты.",
            examples=["service@example.com"],
        ),
    ],
    session: SessionDep,
):
    # Проверяем, если email предоставлен
    if not query.email:
        raise HTTPException(status_code=403, detail="Email is required")

    token = await get_token_from_db(query.email, session=session)

    if not token:
        raise HTTPException(status_code=403, detail="Token not found")

    return {"access_token": token, "token_type": "bearer", "email": query.email}


@router.post(
    "/create-refresh", summary="Создать или обновить токен", response_model=TokenModel
)
async def create_or_refresh_token(request: TokenRequestModel, session: SessionDep):

    # Проверяем, если email предоставлен
    if not request.email:
        raise HTTPException(status_code=403, detail="Email is required")

    # Создаем токен
    email = request.email.lower()
    user_data = {"sub": email}
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = await create_access_token(
        data=user_data, expires_delta=access_token_expires
    )

    # Сохранение токена в базе данных
    await save_token_to_db(email=email, token=access_token, session=session)

    return {"access_token": access_token, "token_type": "bearer", "email": email}
