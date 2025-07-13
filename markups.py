from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from settings import (
    next_race_button_text,
    schedule_button_text,
    track_button_text,
    standings_button_text,
    teams_button_text,
    results_button_text,
    last_race_button_text,
    last_qualy_button_text,
    last_sprint_button_text,
    last_sprint_qualy_button_text,
    list_of_users_button_text,
    number_of_users_button_text,
    parser_data_button_text,
    parser_reload_button_text,
    notifications_reload_button_text
)
from parser.schedule import parse_last_sprint_qualy


# Основные кнопки
next_race_button = KeyboardButton(text=next_race_button_text)
schedule_button = KeyboardButton(text=schedule_button_text)
track_button = KeyboardButton(text=track_button_text)
standings_button = KeyboardButton(text=standings_button_text)
teams_button = KeyboardButton(text=teams_button_text)
results_button = KeyboardButton(text=results_button_text)

# Кнопки для последней гонки
last_race_button = KeyboardButton(text=last_race_button_text)
last_qualy_button = KeyboardButton(text=last_qualy_button_text)
last_sprint_button = KeyboardButton(text=last_sprint_button_text)
last_sprint_qualy_button = KeyboardButton(text=last_sprint_qualy_button_text)
back_button = KeyboardButton(text='Назад')

# Кнопки админа
list_of_users_button = KeyboardButton(text=list_of_users_button_text)
number_of_users_button = KeyboardButton(text=number_of_users_button_text)
parser_data_button = KeyboardButton(text=parser_data_button_text)
parser_reload_button = KeyboardButton(text=parser_reload_button_text)
notifications_reload_button = KeyboardButton(text=notifications_reload_button_text)


home_layout = [
    [schedule_button],
    [standings_button, next_race_button],
    [teams_button, track_button],
    [results_button]
]

results_layout = [
    [last_race_button],
    [last_qualy_button],
    [back_button]
]

results_with_sprint_layout = [
    [last_sprint_button, last_race_button],
    [last_sprint_qualy_button, last_qualy_button],
    [back_button]
]

admin_layout = [
    [list_of_users_button, parser_data_button],
    [number_of_users_button, parser_reload_button],
    [notifications_reload_button],
    [back_button]
]


home_markup = ReplyKeyboardMarkup(keyboard=home_layout)
results_markup = ReplyKeyboardMarkup(keyboard=results_layout)
results_with_sprint_markup = ReplyKeyboardMarkup(keyboard=results_with_sprint_layout)
admin_markup = ReplyKeyboardMarkup(keyboard=admin_layout)


def get_results_markup() -> ReplyKeyboardMarkup:
    '''Возвращает маркап результатов последней гонки в зависимости от того, был ли спринт'''

    if parse_last_sprint_qualy() != 404:
        return results_with_sprint_markup
    return results_markup
