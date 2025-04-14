from aiogram.fsm.state import StatesGroup, State


class Client(StatesGroup):
    id = State()
    name = State()
    lastname = State()
    patronymic = State()
    city_id = State()
    number = State()


class UpdateClient(StatesGroup):
    user_id = State()
    name = State()
    lastname = State()
    number = State()
