import asyncio
import logging


from aiogram import Bot
from aiogram import Dispatcher
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from database.crud.couriers_crud import test_courier
from database.crud.kitchens_crud import delete_kitchen, test
from database.crud.orders_crud import create_order, create_order_assoc
from database.crud.product_crud import create_product
from database.models import Base, OrderProductAssociation
from database.engine import engine, drop_db

from config import BOT_TOKEN
from routers import router as main_router



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(main_router)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def main():
    await drop_db()
    await create_db()
    await create_order_assoc()


    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

