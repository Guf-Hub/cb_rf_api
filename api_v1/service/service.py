import asyncio
import logging
from datetime import datetime
import pytz

import aiohttp
import requests
import xml.etree.ElementTree as ET

from api_v1.db.crud import truncate_table
from api_v1.db.models.models import ExchangeRate
from api_v1.service.models.models import CurrencyCodeModel, ExchangeRateModel

from utils.utils import get_random_user_agent

timezone = "Europe/Moscow"
tz = pytz.timezone(timezone)


async def currency_codes(json_list: bool = False) -> list | dict:
    url = "https://www.cbr.ru/scripts/XML_valFull.asp"

    currency = []
    json_list_data = {}
    for attempt in range(5):  # Число попыток
        try:
            async with aiohttp.ClientSession() as aiohttp_session:
                async with aiohttp_session.get(
                    url, headers={"User-Agent": get_random_user_agent()}
                ) as response:

                    if response.status == 200:
                        response = await response.text()

                        root = ET.fromstring(response)

                        # Извлечение данных
                        for item in root.findall("Item"):
                            cb_code = item.get("ID")
                            iso_id = item.find("ISO_Num_Code").text
                            iso_code = item.find("ISO_Char_Code").text
                            name_ru = item.find("Name").text
                            name_eng = item.find("EngName").text
                            nominal = item.find("Nominal").text

                            if json_list:
                                json_list_data[cb_code] = {
                                    "iso_id": int(iso_id) if iso_id else None,
                                    "iso_code": iso_code if iso_code else None,
                                    "name_ru": name_ru if name_ru else None,
                                    "name_eng": name_eng if name_eng else None,
                                }

                            else:
                                currency.append(
                                    CurrencyCodeModel(
                                        cb_code=cb_code,
                                        iso_id=int(iso_id) if iso_id else None,
                                        iso_code=iso_code if iso_code else None,
                                        name_ru=name_ru if name_ru else None,
                                        name_eng=name_eng if name_eng else None,
                                        nominal=int(nominal) if nominal else None,
                                    ).to_dict()
                                )
                        break
        except aiohttp.ClientConnectorError as e:
            print(f"Попытка {attempt + 1}: Не удалось установить соединение. {e}")
            await asyncio.sleep(2)  # Задержка перед повторной попыткой
    if json_list:
        return json_list_data
    return currency


async def exchange_rates_daly(date: str = None, currency_iso_code: str = None) -> list:
    url = (
        f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={datetime.fromisoformat(date).strftime("%d/%m/%Y")}"
        if date
        else f"http://www.cbr.ru/scripts/XML_daily.asp"
    )

    currency = []

    for attempt in range(5):  # Число попыток
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, headers={"User-Agent": get_random_user_agent()}
                ) as response:
                    if response.status == 200:
                        response = await response.text()

                        root = ET.fromstring(response)
                        date = (
                            datetime.strptime(root.get("Date"), "%d.%m.%Y")
                            .date()
                            .strftime("%Y-%m-%d")
                        )

                        # Извлечение данных
                        for record in root.findall("Valute"):
                            cb_code = record.get("ID")
                            iso_id = record.find("NumCode").text
                            iso_code = record.find("CharCode").text
                            name_ru = record.find("Name").text
                            nominal = record.find("Nominal").text
                            value = record.find("Value").text
                            unit_rate = record.find("VunitRate").text

                            currency_ = ExchangeRateModel(
                                date=date,
                                cb_code=cb_code,
                                iso_id=int(iso_id) if iso_id else None,
                                iso_code=iso_code,
                                name_ru=name_ru,
                                nominal=int(nominal) if nominal else None,
                                value=value,  # float(value.replace(',', '.')) if value else 0,
                                unit_rate=unit_rate,  # float(unit_rate.replace(',', '.')) if unit_rate else 0,
                            ).to_dict()

                            currency.append(currency_)
                        break

        except aiohttp.ClientConnectorError as e:
            print(f"Попытка {attempt + 1}: Не удалось установить соединение. {e}")
            await asyncio.sleep(2)  # Задержка перед повторной попыткой

    if currency_iso_code:
        currency = [c for c in currency if c["iso_code"] == currency_iso_code]

    return currency


async def exchange_rates_dynamics(date_from=None, date_to=None, cb_code_codes=None):
    # Загрузка кодов валют
    currency_json = await currency_codes(json_list=True)

    # Определение начальной и конечной дат
    start_date = (
        datetime.fromisoformat(date_from).strftime("%d/%m/%Y")
        if date_from
        else "01/07/1992"
    )
    end_date = (
        datetime.fromisoformat(date_to).strftime("%d/%m/%Y")
        if date_to
        else datetime.now(tz=tz).strftime("%d/%m/%Y")
    )

    # Если коды валют не переданы, извлекаем их из currency_json
    cb_code_codes = cb_code_codes if cb_code_codes else currency_json.keys()

    currency = []

    async with aiohttp.ClientSession() as aiohttp_session:
        tasks = []

        for parent_code in cb_code_codes:
            url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={end_date}&VAL_NM_RQ={parent_code}"
            tasks.append(fetch_currency_data(aiohttp_session, url, currency_json))

        # Ожидание завершения всех асинхронных задач
        results = await asyncio.gather(*tasks)
        for result in results:
            currency.extend(result)
        print(f"Всего валют: {currency}")

    return currency


async def fetch_currency_data(session, url, currency_json):

    for attempt in range(5):  # Число попыток
        try:
            async with session.get(
                url, headers={"User-Agent": get_random_user_agent()}
            ) as response:

                if response.status != 200:
                    return []

                response_text = await response.text()
                root = ET.fromstring(response_text)

                return [
                    ExchangeRateModel(
                        date=record.get("Date"),
                        cb_code=record.get("Id"),
                        iso_id=currency_json[record.get("Id")].get("iso_id"),
                        iso_code=currency_json[record.get("Id")].get("iso_code"),
                        name_ru=currency_json[record.get("Id")].get("name_ru"),
                        nominal=(
                            int(record.find("Nominal").text)
                            if record.find("Nominal") is not None
                            else None
                        ),
                        value=record.find("Value").text,
                        unit_rate=record.find("VunitRate").text,
                    ).to_dict()
                    for record in root.findall("Record")
                    if currency_json[record.get("Id")] is not None
                ]
        except aiohttp.ClientConnectorError as e:
            print(f"Попытка {attempt + 1}: Не удалось установить соединение. {e}")
            await asyncio.sleep(2)  # Задержка перед повторной попыткой
        return []  # Возврат None после исчерпания всех попыток


async def period_exchange_rates(
    session, date_from=None, date_to=None, cb_code_codes: list[str] = None
) -> list[ExchangeRate]:
    start_date = (
        datetime.fromisoformat(date_from).strftime("%d/%m/%Y")
        if date_to
        else "01/01/2004"
    )
    end_date = (
        datetime.fromisoformat(date_to).strftime("%d/%m/%Y")
        if date_to
        else datetime.now().strftime("%d/%m/%Y")
    )

    if not cb_code_codes:
        cb_code_codes = [
            "R01239",  # EUR
            "R01235",  # USD
            "R01375",  # CNY
            "R01700J",  # TRY Турецкая лира
            # СНГ
            "R01060",  # AMD Армянский драм
            "R01090",  # BYR Белорусский рубль
            "R01335",  # KZT Казахстанский тенге
            "R01370",  # KGS Киргизский сом
            "R01670",  # TJS Таджикский сомони
            "R01717",  # UZS Узбекский сум
            "R01720",  # UAH Украинская гривна
            "R01020A",  # AZN Азербайджанский манат
            "R01210",  # GEL Грузинский лари
        ]

    iso_codes: dict = {
        "R01239": "EUR",
        "R01235": "USD",
        "R01375": "CNY",
        "R01370": "KGS",
        "R01335": "KZT",
        "R01090": "BYR",
        "R01060": "AMD",
        "R01670": "TJS",
        "R01700J": "TRY",
        "R01717": "UZS",
        "R01720": "UAH",
        "R01020A": "AZN",
        "R01210": "GEL",
    }

    currency = []
    for parent_code in cb_code_codes:
        url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={end_date}&VAL_NM_RQ={parent_code}"

        response = requests.get(url)

        root = ET.fromstring(response.text)

        # Извлечение данных
        for record in root.findall("Record"):
            date = record.get("Date")
            cb_code = record.get("Id")
            nominal = record.find("Nominal").text
            value = record.find("Value").text
            unit_rate = record.find("VunitRate").text
            iso_code = iso_codes.get(parent_code)

            currency.append(
                ExchangeRate(
                    date=datetime.strptime(date, "%d.%m.%Y").date(),
                    cb_code=cb_code,
                    nominal=int(nominal) if nominal else None,
                    value=value,  # float(value.replace(',', '.')) if value else 0,
                    unit_rate=unit_rate,  # float(unit_rate.replace(',', '.')) if unit_rate else 0,
                    iso_code=iso_code,
                )
            )

    added_count = 0

    await truncate_table(ExchangeRate)
    await session.add_all(currency)
    await session.commit()
    added_count += len(currency)

    logging.info("Added: %s", added_count)

    return currency
