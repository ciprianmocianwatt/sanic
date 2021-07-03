from functools import lru_cache

from pydantic import BaseSettings
from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()


class DefaultSettings(BaseSettings):
    # application settings
    app_name: str
    debug_mode: bool

    # server settings
    proxy_secret: str = "secret"

    # database settings
    DB_USED: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    db_url: str = ""


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_url = f'{self.DB_USED}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        case_sensitive = True
        env_prefix = 'app_name_'
        fields = {
            'app_name': {
                'env': 'app_name',
            },
            'debug_mode': {
                'env': 'debug_mode'
            },
            'DB_USED': {
                'env': 'DB_USED',
            },
            'DB_USER': {
                'env': 'DB_USER',
            },
            'DB_PASSWORD': {
                'env': 'DB_PASSWORD',
            },
            'DB_HOST': {
                'env': 'DB_HOST',
            },
            'DB_PORT': {
                'env': 'DB_PORT',
            },
            'DB_NAME': {
                'env': 'DB_NAME',
            }
        }


def setup_database(settings: DefaultSettings):
    engine = create_async_engine(
        settings.db_url, echo=True, poolclass=NullPool
    )
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return engine, async_session


async def shutdown_database(app: Sanic):
    db = app.ctx.engine
    await db.dispose()


@lru_cache
def get_base_settings(settings: BaseSettings = None) -> DefaultSettings:
    if not settings:
        return DefaultSettings()
    return settings
