from pathlib import Path

from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB = os.getenv("DB_LITE")
ADMINS = os.getenv("ADMINS")
BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    db_url: str = f"{DB}"
    db_echo: bool = False
    admins: list[int] = ADMINS


settings = Setting()
