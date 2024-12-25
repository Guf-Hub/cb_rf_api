from typing import Annotated, Union
from datetime import datetime
import pytz

from fastapi import (
    APIRouter,
    Query,
    HTTPException,
    status,
    Body,
)


from core.dependencies import TokenDep
from .models.models import (
    TotalExchangeRateModel,
    TotalCurrencyCodeModel,
    CBCodesRequestModel,
)
from .service import currency_codes, exchange_rates_daly, exchange_rates_dynamics

router = APIRouter()

timezone = "Europe/Moscow"
tz = pytz.timezone(timezone)


@router.get(
    "/code-reference",
    tags=["Directory"],
    status_code=status.HTTP_200_OK,
    summary="Получить справочник включающий ISO коды валют",
    response_model=TotalCurrencyCodeModel,
    dependencies=[TokenDep],
)
async def get_code_reference():

    result = await currency_codes()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Not content",
            headers={"response": "Not content"},
        )

    return {"total": len(result), "items": result}


@router.get(
    "/exchange-rates/daily",
    tags=["Exchange"],
    status_code=status.HTTP_200_OK,
    summary="Получить котировки валют на заданный день",
    response_model=TotalExchangeRateModel,
    dependencies=[TokenDep],
)
async def get_exchange_rates_daly(
    date: Annotated[
        Union[str, None],
        Query(
            alias="date",
            title="string",
            examples=["2024-01-01"],
            description="Дата в формате `RFC3339`. "
            "Если параметр отсутствует или на дату небыли установлены котировки, "
            "в ответе будут данные на последнюю зарегистрированную дату. "
            "Минимальная дата: 1992-07-01.",
            min_length=10,
            pattern="^\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}Z)?",
        ),
    ] = None,
    currency_iso_code: Annotated[
        Union[str, None],
        Query(
            alias="currency_iso_code",
            title="string",
            examples=["USD"],
            description="ISO код валюты",
        ),
    ] = None,
):

    if date:
        if datetime.strptime(date, "%Y-%m-%d").date() > datetime.now(tz=tz).date():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date > current date",
            )

    result = await exchange_rates_daly(date, currency_iso_code)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Not content",
            headers={"response": "Not content"},
        )

    return {"total": len(result), "items": result}


@router.post(
    "/exchange-rates/dynamics",
    tags=["Exchange"],
    status_code=status.HTTP_200_OK,
    summary="Получить динамику котировок по кодам валют ЦБ РФ",
    response_model=TotalExchangeRateModel,
    dependencies=[TokenDep],
)
async def get_exchange_rates_dynamics(
    request: Annotated[
        CBCodesRequestModel,
        Body(
            alias="cb_codes",
            title="Array of string",
            examples=[
                {
                    "cb_codes": [
                        "R01239",
                        "R01235",
                    ]
                }
            ],
            description="Список кодов валют ЦБ РФ. Получить коды: `/get/code-reference`. "
            "Минимальное кол-во: 1. "
            "Максимальное кол-во: 15.",
            min_items=1,
            max_items=15,
        ),
    ],
    date_from: Annotated[
        Union[str, None],
        Query(
            alias="date_from",
            title="string",
            examples=["2024-01-01"],
            description="Дата в формате `RFC3339` с ... "
            "По умолчанию: 1992-07-01. "
            "Минимальная дата: 1992-07-01.",
            min_length=10,
            pattern="^\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}Z)?",
        ),
    ] = None,
    date_to: Annotated[
        Union[str, None],
        Query(
            alias="date_to",
            title="string",
            examples=["2024-01-31"],
            description="Дата в формате `RFC3339` по ... "
            "По умолчанию: текущая дата. "
            "Минимальная дата: 1992-07-01.",
            min_length=10,
            pattern="^\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}Z)?",
        ),
    ] = None,
):

    if date_from and not date_to:
        if datetime.strptime(date_from, "%Y-%m-%d").date() > datetime.now(tz=tz).date():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from > current date",
            )

    if date_from and date_to:
        if (
            datetime.strptime(date_from, "%Y-%m-%d").date()
            > datetime.strptime(date_to, "%Y-%m-%d").date()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from > date_to",
            )

    result = await exchange_rates_dynamics(
        date_from,
        date_to,
        request.cb_codes if request else None,
    )

    print(result)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Not content",
            headers={"response": "Not content"},
        )

    return {"total": len(result), "items": result}
