from aiogram.fsm.state import StatesGroup, State


class Courier(StatesGroup):
    user_id = State()
    name = State()
    lastname = State()
    number = State()
    city_id = State()

class UpdateCourier(StatesGroup):
    user_id = State()
    name = State()
    lastname = State()
    number = State()
    city_id = State()