import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    schedule_ans,
    schedule_template,
    schedule_locations_translation
)
from parser.schedule import get_schedule
from markups import home_markup
from utils import msk


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
            schedule_locations_translation[event['Country'] if event['Country'] not in ['United States', 'Spain'] else event['Location']],
            event['EventDate'].strftime('%d\\.%m'),
            msk(event['Session5DateUtc']).strftime('%H:%M'),
            msk(event['Session4DateUtc']).strftime('%H:%M')
        )

        if event['Session3'] == 'Sprint':
            ans += '>    Спринт: {}   Спринт квала: {}\n'.format(
                msk(event['Session3DateUtc']).strftime('%H:%M'),
                msk(event['Session2DateUtc']).strftime('%H:%M'),
            )
        
        ans += '\n'

    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)
