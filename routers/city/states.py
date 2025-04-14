from aiogram.fsm.state import StatesGroup, State


class City(StatesGroup):
    title = State()

class ChangeCity(StatesGroup):
    id = State()
    title = State()