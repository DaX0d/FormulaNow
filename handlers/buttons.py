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
    last_qualy_button_text
)

from .last_race import (
    last_race_handler,
    last_qualy_handler,
    results_menu_handler
)
from .next_race import next_race_handler, track_handler
from .schedule import schedule_handler
from .standings import standings_handler, teams_handler
from markups import home_markup


buttons_router = Router(name='buttons')


@buttons_router.message()
async def buttons_handler(message: Message):
    '''Вызывает хендлер, соответствующий нажатой кновке'''

    if message.text == next_race_button_text:
        await next_race_handler(message)
    elif message.text == schedule_button_text:
        await schedule_handler(message)
    elif message.text == track_button_text:
        await track_handler(message)
    elif message.text == standings_button_text:
        await standings_handler(message)
    elif message.text == teams_button_text:
        await teams_handler(message)
    elif message.text == results_button_text:
        await results_menu_handler(message)
    elif message.text == last_race_button_text:
        await last_race_handler(message)
    elif message.text == last_qualy_button_text:
        await last_qualy_handler(message)
    elif message.text == 'Назад':
        await message.answer('Главное меню', reply_markup=home_markup)
    else:
        await message.answer('Действие не распознано', reply_markup=home_markup)
