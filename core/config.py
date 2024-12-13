import logging
import os
from datetime import timedelta
from pathlib import Path
from typing import Optional, List, Any
from pprint import pformat

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

DIR_PATH = Path(__file__).parent.parent
DB_PATH_SQLITE = os.path.join(DIR_PATH, "database")

if not os.path.exists(DB_PATH_SQLITE):
    os.makedirs(DB_PATH_SQLITE)

CURRENT_PATH = Path(__file__).parent


class DefaultConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


class AuthConfig(DefaultConfig):
    JWT_ALG: str = "HS256"
    JWT_SECRET: Optional[str] = None
    JWT_EXP: int = 365

    REFRESH_TOKEN_KEY: Optional[str] = None
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)

    SECURE_COOKIES: bool = True


class UvicornConfig(DefaultConfig):
    APP: str = "main:app"
    HOST: str = "localhost"  # "0.0.0.0"
    PORT: int = 80  # 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    WORKERS: int = 5

    @property
    def uvicorn_kwargs(self) -> dict:
        return {
            "app": self.APP,
            "host": self.HOST,
            "port": self.PORT,
            "reload": self.RELOAD,
            "log_level": self.LOG_LEVEL,
            "workers": self.WORKERS,
        }


class DBSettings(DefaultConfig):
    SQLITE_AIO_SYSTEM: str = "sqlite"
    SQLITE_AIO_DRIVER: str = "aiosqlite"
    SQLITE_AIO_DB: str = f"{DB_PATH_SQLITE}/db.db"

    ECHO: bool = False

    POSTGRES_SYSTEM: Optional[str] = None
    POSTGRES_DRIVER: Optional[str] = None

    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None

    PGADMIN_EMAIL: Optional[str] = None
    PGADMIN_PASSWORD: Optional[str] = None
    PGADMIN_CONFIG_SERVER_MODE: Optional[bool] = None

    @property
    def url_sqlite(self) -> str:
        """Build a connection string for AioSQLite"""
        return URL.create(
            drivername=f"{self.SQLITE_AIO_SYSTEM}+{self.SQLITE_AIO_DRIVER}",
            database=self.SQLITE_AIO_DB.replace("\\", "/"),  # Заме,
        ).render_as_string()

    @property
    def url_postgres(self) -> str:
        """Build a connection string for PostgreSQL"""
        return URL.create(
            drivername=f"{self.POSTGRES_SYSTEM}+{self.POSTGRES_DRIVER}",
            username=self.POSTGRES_USER,
            database=self.POSTGRES_DB,
            password=self.POSTGRES_PASSWORD,
            port=self.POSTGRES_PORT,
            host=self.POSTGRES_HOST,
        ).render_as_string(hide_password=False)


class Settings(BaseSettings):
    dev: bool = True
    api: bool = False
    use_sqlite: bool = True
    api_v1_prefix: str = "/api/v1"
    auth: AuthConfig = AuthConfig()
    db: DBSettings = DBSettings()
    uvicorn: UvicornConfig = UvicornConfig()

    def show(self):
        logging.info("Settings:\n", pformat(self.model_dump()))


settings = Settings()
