import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from settings import *
from markups import home_markup
from parser import (
    get_schedule,
    get_next_race, 
    parse_all, 
    get_standings,
    get_last_race
    )


load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()


def msk(t: str) -> str:
    '''Принимает время по гринвичу, возвращает по московскому времени'''
    h = (int(t[:2].lstrip('0') or '0') + 3) % 24
    return '{:02d}{}'.format(h, t[2:])


def prev_date(day, month, d) -> tuple[int, int]:
    '''Принимает дату (день и месяц), возвращает дату, отмотанную назад на указанное кол-во дней в виде кортежа'''

    if day - d > 0:
        return (day - d, month)
    
    new_month = month - 1

    if new_month - 1 < 8:
        match new_month % 2:
            case 0:
                return (day - d + 30, new_month)
            case 1:
                return (day - d + 31, new_month)
    else:
        match new_month % 2:
            case 0:
                return (day - d + 31, new_month)
            case 2:
                return (day - d + 30, new_month)


@dp.message(Command('start'))
async def start_handler(message: Message):
    '''Отправляет приветственное сообщение'''
    await message.answer(start_ans, reply_markup=home_markup)


@dp.message(Command('next'))
async def next_race_handler(message: Message):
    '''Отправляет расписание следующей гонки'''

    ans = next_race_ans
    next_race = get_next_race()
    day, month = map(int, next_race['race_date'].split('.'))

    if next_race['schedule']['sprintRace']['time']:
        fp2_n = 'Квалификация к спринту'
        fp2_t = msk(next_race['schedule']['sprintQualy']['time'][:-4])
        fp3_n = 'Спринт'
        fp3_t = msk(next_race['schedule']['sprintRace']['time'][:-4])
    else:
        fp2_n = 'Практика 2'
        fp2_t = msk(next_race['schedule']['fp2']['time'][:-4])
        fp3_n = 'Практика 3'
        fp3_t = msk(next_race['schedule']['fp3']['time'][:-4])
    
    information = next_race_template.format(
        name=next_race['name'],
        fr_date='{:02d}\\.{:02d}'.format(*prev_date(day, month, 2)),
        sat_date='{:02d}\\.{:02d}'.format(*prev_date(day, month, 1)),
        sun_date='{:02d}\\.{:02d}'.format(day, month),
        fp1_t=msk(next_race['schedule']['fp1']['time'][:-4]),
        fp2_t=fp2_t,
        fp3_t=fp3_t,
        q_t=msk(next_race['schedule']['qualy']['time'][:-4]),
        r_t=msk(next_race['schedule']['race']['time'][:-4]),
        fp2_n=fp2_n,
        fp3_n=fp3_n
    )

    ans += information

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)


@dp.message(Command('schedule'))
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


@dp.message(Command('track'))
async def track_handler(message: Message):
    '''Отправляет информацию о треке, на котором следующая гонка'''

    next_race = get_next_race()
    photo_file = FSInputFile(f'./static/{track_photoes[grand_prix_locations.index(next_race['name'])]}.jpg')

    ans = track_ans + track_template.format(
        next_race['name'],
        next_race['track']['circuitName'],
        next_race['track']['city'],
        next_race['track']['circuitLength'][:-2] + ' м',
        next_race['gp']['laps'],
        next_race['track']['corners']
    )

    await message.answer_photo(photo_file, parse_mode='MarkdownV2', caption=ans, reply_markup=home_markup)


@dp.message(Command('standings'))
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


@dp.message(Command('teams'))
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


@dp.message(Command('last'))
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


@dp.message()
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
    elif message.text == last_race_button_text:
        await last_race_handler(message)
    else:
        await message.answer('Действие не распознано')


async def periodic_parser():
    '''Функция, периодически вызывающая парсер всех данных'''

    while True:
        parse_all()
        await asyncio.sleep(PARSE_DELAY)


async def main():
    '''Запускает бота и парсер параллельно'''

    asyncio.create_task(periodic_parser())
    logging.info('Bot started')

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Exiting')
