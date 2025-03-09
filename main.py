import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Holla"
    )
    await message.answer(text=message.text)



async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

