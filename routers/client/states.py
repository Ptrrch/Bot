from aiogram.fsm.state import StatesGroup, State


class Client(StatesGroup):
    name = State()
    lastname = State()
    number = State()


class UpdateClient(StatesGroup):
    user_id = State()
    name = State()
    lastname = State()
    number = State()
