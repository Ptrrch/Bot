import asyncio
import logging
from datetime import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio


from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.crud.couriers_crud import get_couriers, change_courier_counter
from database.models import Base
from database.engine import engine

from database.config import BOT_TOKEN
from routers import router as main_router



bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties( parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(main_router)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)






async def main():
    await create_db()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(change_courier_counter, 'cron', hour=0, minute=0)
    scheduler.start()


    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

