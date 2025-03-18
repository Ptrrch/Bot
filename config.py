from pathlib import Path

from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True


settings = Setting()
