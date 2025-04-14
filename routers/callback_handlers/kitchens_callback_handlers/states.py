from aiogram.fsm.state import StatesGroup, State


class Change(StatesGroup):
    product = State()
    address = State()
    payments_type = State()
    change_amount = State()

class ChangeOrder(StatesGroup):
    order_id = State()
    address = State()
    payments_type = State()
    change_amount = State()
    delivery_time = State()