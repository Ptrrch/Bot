from aiogram.fsm.state import StatesGroup, State


class Courier(StatesGroup):
    name = State()
    lastname = State()
    number = State()
    city_id = State()