from typing import List

from pydantic import BaseSettings

from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL = "sqlite+aiosqlite:///./my.db"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = "QknXsGf_6K3e2lLflPvlaknjkEPKbKRt5kBIDuDDFWc"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 60 min * 24 horas * 7 dias

    class Config:
        case_sensitive = True


settings: Settings = Settings()
