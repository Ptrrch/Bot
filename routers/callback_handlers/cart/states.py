from aiogram.fsm.state import StatesGroup, State


class Cart(StatesGroup):
    product_id = State()
