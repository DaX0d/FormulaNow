import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from settings import *
from markups import home_markup
from parser import get_schedule, get_next_race, parse_all, get_standings

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()

def msk(t: str) -> str:
    h = (int(t[:2].lstrip('0') or '0') + 3) % 24
    return '{:02d}{}'.format(h, t[2:])

def prev_date(day, month, d) -> tuple[int, int]:
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
    await message.answer(start_ans, reply_markup=home_markup)

@dp.message(Command('next'))
async def next_race_handler(message: Message):
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
    await message.answer(ans, parse_mode='MarkdownV2')

@dp.message(Command('schedule'))
async def schedule_handler(message: Message):
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
    await message.answer(ans, parse_mode='MarkdownV2')

@dp.message(Command('track'))
async def track_handler(message: Message):
    await message.answer(track_ans)

@dp.message(Command('standings'))
async def standings_handler(message: Message):
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
    await message.answer(ans, parse_mode='MarkdownV2')

@dp.message(Command('teams'))
async def teams_handler(message: Message):
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
    await message.answer(ans, parse_mode='MarkdownV2')

@dp.message()
async def buttons_handler(message: Message):
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
    else:
        await message.answer('Действие не распознано')

async def periodic_parser():
    while True:
        parse_all()
        print('Начало ожидания')
        await asyncio.sleep(PARSE_DELAY)

async def main():
    asyncio.create_task(periodic_parser())
    print('Бот запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exiting')
