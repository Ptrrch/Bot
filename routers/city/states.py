from aiogram.fsm.state import StatesGroup, State


class City(StatesGroup):
    tittle = State()

class ChangeCity(StatesGroup):
    id = State()
    tittle = State()