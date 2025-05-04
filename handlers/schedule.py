from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    schedule_ans,
    schedule_template
)
from parser import get_schedule
from markups import home_markup
from utils import msk


schedule_router = Router(name='schedule_router')


@schedule_router.message(Command('schedule'))
async def schedule_handler(message: Message):
    '''Отправляет все расписание'''

    schedule = get_schedule()
    ans = schedule_ans

    for i in range(len(schedule)):
        ans += schedule_template.format(
            i + 1,
            schedule[i]['name'],
            f'{schedule[i]['date'][-2:]}\\.{schedule[i]['date'][5:7]}',
            msk(schedule[i]['race_time']),
            msk(schedule[i]['q_time'])
        )

        if schedule[i]['sprint_time']:
            ans += '>    Спринт: {}   Спринт квала: {}\n'.format(
                msk(schedule[i]['sprint_time'][:-4]),
                msk(schedule[i]['sq_time'][:-4])
            )
        
        ans += '\n'

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)
