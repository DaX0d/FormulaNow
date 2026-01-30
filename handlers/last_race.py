from types import NoneType
import datetime
import pandas as pd
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
    grand_prix_dict,
    driver_translation,
    schedule_locations_translation
)
from parser.schedule import (
    get_last_race,
    get_last_qualy,
    get_last_sprint,
    get_last_sprint_qualy
)
from markups import get_results_markup
from utils import translate_location_from_session, tg_format, format_lap_time


last_race_router = Router(name='last_race')


@last_race_router.message(Command('results'))
async def results_menu_handler(message: Message):
    '''Выводит клавиатуру с результатами предыдущей гонки'''

    ans = results_ans

    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=get_results_markup())


@last_race_router.message(Command('race'))
async def last_race_handler(message: Message):
    '''Отправляет результаты последней гонки'''

    last_race = get_last_race()
    ans = last_race_ans

    if not isinstance(last_race, NoneType):
        last_race.load(laps=False, telemetry=False, weather=False, messages=False, livedata=False)
        driver = lambda n: driver_translation[last_race.results.iat[n, 3]]
        race_name = translate_location_from_session(last_race)

        winner = '>*1.🥇 {}*\n'.format(driver(0))
        second = '>*2.🥈 {}*\n'.format(driver(1))
        third = '>*3.🥉 {}*\n\n'.format(driver(2))

        other = ''
        for i in range(3, len(last_race.results.index)):
            other += '>{}. {} {}\n'.format(
                i + 1,
                driver(i),
                ''
            )

        ans += f'*{race_name}*\n\n' + winner + second + third + other
    else:
        ans += 'Пока что нет данных'

    return await message.answer(tg_format(ans), parse_mode='MarkdownV2', reply_markup=get_results_markup())


@last_race_router.message(Command('qualy'))
async def last_qualy_handler(message: Message):
    '''Отправляет результаты последней квалификации'''

    last_qualy = get_last_qualy()
    ans = last_qualy_ans
    if not isinstance(last_qualy, NoneType):
        last_qualy.load(laps=False, telemetry=False, weather=False, messages=False, livedata=False)
        driver = lambda n: driver_translation[last_qualy.results.iat[n, 3]]
        race_name = translate_location_from_session(last_qualy)

        pole = f'>*1. {driver(0)} - {format_lap_time(last_qualy.results.iloc[0].loc['Q3'])}*\n\n'
        # print(pole)

        grid = ''
        for i in range(1, len(last_qualy.results.index)):
            for segment in ['Q3', 'Q2', 'Q1']:
                time = last_qualy.results.iloc[i].loc[segment]
                if pd.notna(time):
                    grid += '>{:2}. {} - {}\n'.format(
                        i + 1,
                        driver(i),
                        format_lap_time(time)
                    )
                    break

        ans += f'*{race_name}*\n\n' + pole + grid
    else:
        ans += 'Пока что нет данных'
    
    ans = tg_format(ans)
    # print(ans)

    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=get_results_markup())


@last_race_router.message(Command('sprint'))
async def last_sprint_handler(message: Message):
    '''Отрпавляет результаты последнего спринта'''

    last_sprint = get_last_sprint()
    ans = last_sprint_ans

    if not isinstance(last_sprint, NoneType):
        last_sprint.load(laps=False, telemetry=False, weather=False, messages=False, livedata=False)
        driver = lambda n: driver_translation[last_sprint.results.iat[n, 3]]
        race_name = translate_location_from_session(last_sprint)

        winner = '>*1.🥇 {}*\n'.format(driver(0))
        second = '>*2.🥈 {}*\n'.format(driver(1))
        third = '>*3.🥉 {}*\n\n'.format(driver(2))

        other = ''
        for i in range(3, len(last_sprint.results.index)):
            other += '>{}. {} {}\n'.format(
                i + 1,
                driver(i),
                ''
            )

        ans += f'*{race_name}*\n\n' + winner + second + third + other
    else:
        ans += 'Пока что нет данных'

    return await message.answer(tg_format(ans), parse_mode='MarkdownV2', reply_markup=get_results_markup())


@last_race_router.message(Command('s_qualy'))
async def last_sprint_qualy_handler(message: Message):
    '''Отправляет результаты последней спринт квалификации'''

    last_s_qualy = get_last_sprint_qualy()
    ans = last_sprint_qualy_ans
    if not isinstance(last_s_qualy, NoneType):
        last_s_qualy.load(laps=False, telemetry=False, weather=False, messages=False, livedata=False)
        # print(last_s_qualy.results)
        driver = lambda n: driver_translation[last_s_qualy.results.iat[n, 3]]
        race_name = translate_location_from_session(last_s_qualy)

        pole = f'>*1. {driver(0)} - {format_lap_time(last_s_qualy.results.iloc[0].loc['Q3'])}*\n\n'
        # print(pole)

        grid = ''
        for i in range(1, len(last_s_qualy.results.index)):
            for segment in ['Q3', 'Q2', 'Q1']:
                time = last_s_qualy.results.iloc[i].loc[segment]
                if pd.notna(time):
                    grid += '>{:2}. {} - {}\n'.format(
                        i + 1,
                        driver(i),
                        format_lap_time(time)
                    )
                    break

        ans += f'*{race_name}*\n\n' + pole + grid
    else:
        ans += 'Пока что нет данных'
    
    ans = tg_format(ans)
    # print(ans)

    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=get_results_markup())
