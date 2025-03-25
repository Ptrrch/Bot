from aiogram.fsm.state import StatesGroup, State


class Kitchen(StatesGroup):
    title = State()
    description = State()
    number = State()
    address = State()
    city_id = State()