import os
import time
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.formatting import as_numbered_list, Bold, as_line

from settings import *
from markups import home_markup
from parser import get_schedule

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()

def msk(t: str) -> str:
    h = (int(t[:2].lstrip('0') or '0') + 3) % 24
    return '{:02d}{}'.format(h, t[2:])

@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(start_ans, reply_markup=home_markup)

@dp.message(Command('next'))
async def next_race_handler(message: Message):
    await message.answer(next_race_ans)

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
    # print(ans)
    await message.answer(ans, parse_mode='MarkdownV2')

@dp.message(Command('track'))
async def track_handler(message: Message):
    await message.answer(track_ans)

@dp.message(Command('standings'))
async def standings_handler(message: Message):
    await message.answer(standings_ans)

@dp.message(Command('teams'))
async def teams_handler(message: Message):
    await message.answer(teams_ans)

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

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exiting')
