from aiogram import Router
from aiogram.types import Message

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
from .last_race import (
    last_race_handler,
    last_qualy_handler,
    last_sprint_handler,
    results_menu_handler,
    last_sprint_qualy_handler
)
from .next_race import next_race_handler, track_handler
from .schedule import schedule_handler
from .standings import standings_handler, teams_handler
from .admin import (
    list_of_users_handler,
    number_of_users_handler,
    parser_data_handler,
    reload_parser_handler,
    reload_notifications_handler
)
from markups import home_markup


buttons_router = Router(name='buttons')

buttons_dict = {
    next_race_button_text: next_race_handler,
    schedule_button_text: schedule_handler,
    track_button_text: track_handler,
    standings_button_text: standings_handler,
    teams_button_text: teams_handler,
    results_button_text: results_menu_handler,
    last_race_button_text: last_race_handler,
    last_qualy_button_text: last_qualy_handler,
    last_sprint_button_text: last_sprint_handler,
    last_sprint_qualy_button_text: last_sprint_qualy_handler,
    list_of_users_button_text: list_of_users_handler,
    number_of_users_button_text: number_of_users_handler,
    parser_data_button_text: parser_data_handler,
    parser_reload_button_text: reload_parser_handler,
    notifications_reload_button_text: reload_notifications_handler
}


@buttons_router.message()
async def buttons_handler(message: Message):
    '''Вызывает хендлер, соответствующий нажатой кнопке'''

    if message.text in buttons_dict.keys():
        return await buttons_dict[message.text](message)
    elif message.text == 'Назад':
        return await message.answer('Главное меню', reply_markup=home_markup)
    else:
        return await message.answer('Действие не распознано', reply_markup=home_markup)
