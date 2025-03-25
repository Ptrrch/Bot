from aiogram.fsm.state import StatesGroup, State


class Kitchen(StatesGroup):
    title = State()
    description = State()
    number = State()
    address = State()
    cities_id = State()