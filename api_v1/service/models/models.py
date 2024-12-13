from models.base import Model


class CurrencyCodeModel(Model):
    cb_code: str
    iso_id: int | None
    iso_code: str | None
    name_ru: str | None
    name_eng: str | None
    nominal: int | None


class TotalCurrencyCodeModel(Model):
    total: int
    items: list[CurrencyCodeModel]


class ExchangeRateModel(Model):
    date: str
    cb_code: str
    iso_id: int | None
    iso_code: str | None
    name_ru: str | None
    nominal: int | None
    value: str | None
    unit_rate: str | None


class TotalExchangeRateModel(Model):
    total: int
    items: list[ExchangeRateModel]


class CBCodesRequestModel(Model):
    # date_from: str | None
    # date_to: str | None
    cb_codes: list[str]
