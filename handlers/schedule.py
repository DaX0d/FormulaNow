import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    schedule_ans,
    schedule_template,
    DATE_FORMAT,
    TIME_FORMAT
)
from parser.schedule import get_schedule
from markups import home_markup
from utils import msk, translate_location, tg_format


schedule_router = Router(name='schedule_router')


@schedule_router.message(Command('schedule'))
async def schedule_handler(message: Message):
    '''Отправляет все расписание'''

    schedule = get_schedule()
    ans = schedule_ans

    for i in range(len(schedule.index)):
        # schedule_template = '>*{}*  *{}*   *{}*\n>    *Гонка*: {}   Квалификация: {}\n'
        event = schedule.iloc[i]
        ans += schedule_template.format(
            i + 1,
            translate_location(event),
            event['EventDate'].strftime(DATE_FORMAT),
            msk(event['Session5DateUtc']).strftime(TIME_FORMAT),
            msk(event['Session4DateUtc']).strftime(TIME_FORMAT)
        )

        if event['Session3'] == 'Sprint':
            ans += '>    Спринт: {}   Спринт квала: {}\n'.format(
                msk(event['Session3DateUtc']).strftime(TIME_FORMAT),
                msk(event['Session2DateUtc']).strftime(TIME_FORMAT),
            )
        
        ans += '\n'

    return await message.answer(tg_format(ans), parse_mode='MarkdownV2', reply_markup=home_markup)
