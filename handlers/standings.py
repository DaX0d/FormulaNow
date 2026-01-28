from types import NoneType
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    standings_ans,
    teams_ans,
    standings_template,
    teams_template,
    driver_translation
)
from parser.standings import get_drivers, get_teams
from markups import home_markup


standings_router = Router(name='standings_router')


@standings_router.message(Command('standings'))
async def standings_handler(message: Message):
    '''Отправляет таблицу личного зачета'''

    ans = standings_ans
    standings = get_drivers()

    if not isinstance(standings, NoneType):
        for i in range(len(standings.index)):
            driver = standings.iloc[i]
            ans += standings_template.format(
                f'{driver_translation[driver['driverId']]} ({driver['constructorNames'][-1].replace(' F1 Team', '')})',
                int(driver['points'])
            )
    else:
        ans += 'Пока что нет данных'
    
    ans = ans.replace('.', '\\.')
    ans = ans.replace('(', '\\(')
    ans = ans.replace(')', '\\)')

    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)


@standings_router.message(Command('teams'))
async def teams_handler(message: Message):
    '''Отправляет таблицу кубка конструкторов'''

    ans = teams_ans
    teams = get_teams()

    if not isinstance(teams, NoneType):
        for i in range(len(teams.index)):
            team = teams.iloc[i]
            ans += teams_template.format(
                i + 1,
                team['constructorName'],
                int(team['points'])
            )
    else:
        ans += 'Пока что нет данных'
    
    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)
