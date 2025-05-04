from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    standings_ans,
    teams_ans,
    standings_template,
    teams_template
)
from parser import get_standings
from markups import home_markup


standings_router = Router(name='standings_router')


@standings_router.message(Command('standings'))
async def standings_handler(message: Message):
    '''Отправляет таблицу личного зачета'''

    ans = standings_ans
    standings = get_standings()

    i = 1
    for name in standings['racers'].keys():
        ini = name[0]
        short_name = f'{ini}.{name[name.index(' ') + 1:]}'
        ans += standings_template.format(
            i,
            short_name,
            standings['racers'][name]
        )
        i += 1
    
    ans = ans.replace('(', '\\(')
    ans = ans.replace(')', '\\)')

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)


@standings_router.message(Command('teams'))
async def teams_handler(message: Message):
    '''Отправляет таблицу кубка конструкторов'''

    ans = teams_ans
    teams = get_standings()['teams']

    i = 1
    for team in teams.keys():
        ans += teams_template.format(
            i,
            team,
            teams[team]
        )
        i += 1
    
    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)
