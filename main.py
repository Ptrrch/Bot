import asyncio
import logging


from aiogram import Bot,types
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils import markdown

from database.models import Base
from database.engine import engine, drop_db

from config import BOT_TOKEN
from routers import router as main_router



bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties( parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(main_router)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def main():
    # await drop_db()
    await create_db()



    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

