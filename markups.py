from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from settings import *

next_race_button = InlineKeyboardButton(text=next_race_button_text)
schedule_button = InlineKeyboardButton(text=schedule_button_text)

layout = [
    [next_race_button],
    [schedule_button]
]

home_markup = InlineKeyboardMarkup(inline_keyboard=layout)
