from aiogram.fsm.state import StatesGroup, State

class Admin(StatesGroup):
    name = State()
    lastname = State()
    number = State()

class AdminUpdate(StatesGroup):
    name = State()
    lastname = State()
    number = State()

