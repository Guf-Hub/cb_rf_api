from .base import (
    Base,
    Mapped,
    mapped_column,
    int_pk,
    Date,
)


class CurrencyCode(Base):
    """Таблица кодов валют"""

    id: Mapped[int_pk]
    cb_code: Mapped[str | None]
    iso_id: Mapped[int | None]
    iso_code: Mapped[str | None]
    name_ru: Mapped[str | None]
    name_eng: Mapped[str | None]
    nominal: Mapped[int | None]

    repr_cols_num = Base.get_num_keys()


class ExchangeRate(Base):
    """Таблица курсы валют"""

    id: Mapped[int_pk]
    date: Mapped[str | None] = mapped_column(Date, default=None)
    cb_code: Mapped[str]
    iso_code: Mapped[str]
    nominal: Mapped[int]
    value: Mapped[str]
    unit_rate: Mapped[str]

    repr_cols_num = Base.get_num_keys()


class Token(Base):
    """Таблица авторизации"""

    id: Mapped[int_pk]
    email: Mapped[str]
    token: Mapped[str]

    repr_cols_num = Base.get_num_keys()
