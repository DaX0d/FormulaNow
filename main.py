import os
from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from settings import *
from markups import home_markup

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(start_ans, reply_markup=home_markup)

@dp.message(Command('next'))
async def next_race_handler(message: Message):
    await message.answer(next_race_ans)

@dp.message(Command('schedule'))
async def schedule_handler(message: Message):
    await message.answer(schedule_ans)

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
    asyncio.run(main())
