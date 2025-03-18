from aiogram.fsm.state import StatesGroup, State


class Client(StatesGroup):
    name = State()
    lastname = State()
    address = State()
    number = State()
