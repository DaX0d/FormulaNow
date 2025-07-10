from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from settings import (
    last_race_ans,
    last_qualy_ans,
    last_sprint_ans,
    last_sprint_qualy_ans,
    results_ans,
    drivers_shortname_rus,
    grand_prix_dict
)
from parser.schedule import (
    get_last_race,
    get_last_qualy,
    get_last_sprint,
    get_last_sprint_qualy
)
from markups import results_markup, results_with_sprint_markup


last_race_router = Router(name='last_race')


@last_race_router.message(Command('results'))
async def results_menu_handler(message: Message):
    '''Выводит клавиатуру с результатами предыдущей гонки'''

    ans = results_ans

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=results_markup)


@last_race_router.message(Command('race'))
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

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=results_markup)


@last_race_router.message(Command('qualy'))
async def last_qualy_handler(message: Message):
    '''Отправляет результаты последней квалификации'''

    last_qauly = get_last_qualy()
    ans = last_qualy_ans
    driver = lambda n: drivers_shortname_rus[last_qauly['races']['qualyResults'][n]['driver']['shortName']]
    race_name = grand_prix_dict[last_qauly['races']['raceId']]

    pole = f'>*1\\. {driver(0)} \\- {last_qauly['races']['qualyResults'][0]['q3'].replace('.', '\\.')}*\n\n'

    grid = ''
    for i in range(1, 20):
        try:
            grid += '>{}\\. {} \\- {}\n'.format(
                i + 1,
                driver(i),
                last_qauly['races']['qualyResults'][i]['q3'].replace('.', '\\.')
            )
        except:
            try:
                grid += '>{}\\. {} \\- {}\n'.format(
                    i + 1,
                    driver(i),
                    last_qauly['races']['qualyResults'][i]['q2'].replace('.', '\\.')
                )
            except:
                grid += '>{}\\. {} \\- {}\n'.format(
                    i + 1,
                    driver(i),
                    last_qauly['races']['qualyResults'][i]['q1'].replace('.', '\\.')
                )

    ans += f'*{race_name}*\n\n' + pole + grid

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=results_markup)


@last_race_router.message(Command('sprint'))
async def last_sprint_handler(message: Message):
    '''Отрпавляет результаты последнего спринта'''

    last_sprint = get_last_sprint()
    ans = last_sprint_ans
    driver = lambda n: drivers_shortname_rus[last_sprint['races']['sprintRaceResults'][n]['driver']['shortName']]
    race_name = grand_prix_dict[last_sprint['races']['raceId']]

    winner = '>*1\\.🥇 {}*\n'.format(driver(0))
    second = '>*2\\.🥈 {}*\n'.format(driver(1))
    third = '>*3\\.🥉 {}*\n\n'.format(driver(2))

    other = ''
    for i in range(3, 20):
        other += '>{}\\. {} {}\n'.format(
            i + 1,
            driver(i),
            '\\(DNF\\)' if last_sprint['races']['sprintRaceResults'][i]['position'] == 'NC' else ''
        )

    ans += f'*{race_name}*\n\n' + winner + second + third + other

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=results_with_sprint_markup)


@last_race_router.message(Command('s_qualy'))
async def last_sprint_qualy_handler(message: Message):
    '''Отправляет результаты последней спринт квалификации'''
