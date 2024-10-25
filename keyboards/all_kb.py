from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from create_bot import admins
from utils.globals import HOROSCOPE_SIGNS

def create_rat():
    builder = ReplyKeyboardBuilder()
    for item in HOROSCOPE_SIGNS:
        builder.button(text=item)
    builder.adjust(4, 4, 4)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def create_inline():
    inline_kb_list = [[InlineKeyboardButton(text="Обновить гороскоп", callback_data="update")]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
