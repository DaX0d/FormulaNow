from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    last_race_ans,
    drivers_shortname_rus,
    grand_prix_dict
)
from parser import get_last_race
from markups import home_markup


last_race_router = Router(name='last_race')


@last_race_router.message(Command('last'))
async def last_race_handler(message: Message):
    '''Отправляет результаты последней гонки'''

    last_race = get_last_race()
    ans = last_race_ans
    driver = lambda n: drivers_shortname_rus[last_race['races']['results'][n]['driver']['shortName']]
    race_name = grand_prix_dict[last_race['races']['raceId']]

    winner = '>*1\\.🥇 {}*\n'.format(driver(0))
    second = '>*2\\.🥈 {}*\n'.format(driver(1))
    third = '>*3\\.🥉 {}*\n\n'.format(driver(2))

    other = ''
    for i in range(3, 20):
        other += '>{}\\. {} {}\n'.format(
            i + 1,
            driver(i),
            '\\(DNF\\)' if last_race['races']['results'][i]['position'] == 'NC' else ''
        )

    ans += f'*{race_name}*\n\n' + winner + second + third + other

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)
