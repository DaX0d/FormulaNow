import os
import json

from dotenv import load_dotenv

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from markups import admin_markup


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')

admin_router = Router(name='admin')


def user_is_admin(message: Message) -> bool:
    '''Проверяет, является ли пользователь админом'''

    return str(message.from_user.id) == ADMIN_ID


@admin_router.message(Command('admin'))
async def admin_menu_handler(message: Message):
    '''Выводит меню админа'''

    if user_is_admin(message):
        await message.answer('Админское меню', reply_markup=admin_markup)
    else:
        await message.answer('Ты не админ!')


@admin_router.message(Command('list_of_users'))
async def list_of_users_handler(message: Message):
    '''Отпправляет АДМИНУ файл с айди всех пользователей'''

    if user_is_admin(message):
        users_file = FSInputFile('users.json', filename='users.json')
        await message.answer_document(users_file, reply_markup=admin_markup)
    else:
        await message.answer('Ты не админ!')


@admin_router.message(Command('number_of_users'))
async def number_of_users_handler(message: Message):
    '''Выаодит число зарегестрированных пользователей'''

    if user_is_admin(message):
        with open('users.json', 'r', encoding='utf-8') as file:
            users_list = json.load(file)
        await message.answer(f'{len(users_list)}', reply_markup=admin_markup)
    else:
        await message.answer('Ты не админ!')


@admin_router.message(Command('parser_data'))
async def parser_data_handler(message: Message):
    '''Отправляет данные парсера'''

    if user_is_admin(message):
        last = FSInputFile('parser/data/last.json', filename='last.json')
        schedule = FSInputFile('parser/data/schedule.json', filename='schedule.json')
        standings = FSInputFile('parser/data/standings.json', filename='standings.json')

        await message.answer_document(last)
        await message.answer_document(schedule)
        await message.answer_document(standings, reply_markup=admin_markup)
    else:
        await message.answer('Ты не админ!')
