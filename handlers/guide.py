from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from settings import guide_ans
from markups import home_markup


guide_router = Router(name='guide')


@guide_router.message(Command('guide'))
async def guide_handler(message: Message):
    '''Отправляет файл с гайдом по Формуле 1'''

    guide = FSInputFile('static/guide.pdf', filename='Гайд.pdf')

    return await message.answer_document(guide, caption=guide_ans, reply_markup=home_markup)
