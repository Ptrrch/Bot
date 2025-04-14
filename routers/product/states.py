from aiogram.fsm.state import StatesGroup, State


class Product(StatesGroup):
    owned_id = State()
    title = State()
    description = State()
    price = State()
    img = State()


class ChangeProduct(StatesGroup):
    id = State()
    title = State()
    description = State()
    price = State()
    img = State()

