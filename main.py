import os
import asyncio
import logging
import json

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from settings import PARSE_DELAY, start_ans
from markups import home_markup
from parser import parser_task
from handlers import routers
from notifications import notifier_loop, notifications_task


load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()

dp.include_routers(*routers)


@dp.message(Command('start'))
async def start_handler(message: Message):
    '''Отправляет приветственное сообщение и записывает пользователя в список'''

    with open('users.json', 'r', encoding='utf-8') as file:
        all_users = json.load(file)
    
    user_id = str(message.from_user.id)

    if user_id not in all_users:
        all_users.append(user_id)
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(all_users, file)

    await message.answer(start_ans, reply_markup=home_markup)


async def main():
    '''Запускает бота, парсер и рассылку уведомлений параллельно'''

    logging.info('Starting parser')
    parser_task.run()

    logging.info('Starting notifier')
    notifications_task.parametrs = [bot]
    notifications_task.run()

    logging.info('Bot started')

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Exiting')
