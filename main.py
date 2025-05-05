import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from settings import PARSE_DELAY, start_ans
from markups import home_markup
from parser import parse_all
from handlers import routers


load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()

dp.include_routers(*routers)


@dp.message(Command('start'))
async def start_handler(message: Message):
    '''Отправляет приветственное сообщение'''
    await message.answer(start_ans, reply_markup=home_markup)


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
