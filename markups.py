from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from settings import *


next_race_button = KeyboardButton(text=next_race_button_text)
schedule_button = KeyboardButton(text=schedule_button_text)
track_button = KeyboardButton(text=track_button_text)
standings_button = KeyboardButton(text=standings_button_text)
teams_button = KeyboardButton(text=teams_button_text)


layout = [
    [schedule_button],
    [standings_button, next_race_button],
    [teams_button, track_button]
]


home_markup = ReplyKeyboardMarkup(keyboard=layout)
