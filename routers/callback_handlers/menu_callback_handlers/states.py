from aiogram.fsm.state import StatesGroup, State


class Cart(StatesGroup):
    product = State()

class Order(StatesGroup):
    product = State()
    address = State()
    payments_type = State()
    change_amount = State()
    delivery_time = State()