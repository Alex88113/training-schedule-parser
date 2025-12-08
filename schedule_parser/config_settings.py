from pydantic_settings import BaseSettings, SettingsConfigDict
import asyncio
from loggers_module.logger_module import logger
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / '.env'

class AuthSettings(BaseSettings):
    TOP_USERNAME: str
    PASSWORD: str
    APPLICATION_KEY: str
    ID_CITY: str | None =  None

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore' # динамит лишние поля в .env
    )