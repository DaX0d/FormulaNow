import os

from dotenv import load_dotenv

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')

admin_router = Router(name='admin')


@admin_router.message(Command('list_of_users'))
async def list_of_users_handler(message: Message):
    '''Отпправляет АДМИНУ файл с айди всех пользователей'''

    if str(message.from_user.id) == ADMIN_ID:
        users_file = FSInputFile('users.json', filename='users.json')
        await message.answer_document(users_file)
