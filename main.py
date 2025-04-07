import os
from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from answers import *

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(start_ans)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
