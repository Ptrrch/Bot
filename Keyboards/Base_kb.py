from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb():
    kb_list = [
        [KeyboardButton(text="📚 Каталог заведений")],
        [KeyboardButton(text="📖 Мои заказы")],
        [KeyboardButton(text="admin")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard