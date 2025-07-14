import os
from dotenv import load_dotenv
import datetime

from aiogram.types import Message, User, Chat


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')

admin = User(id=int(ADMIN_ID), is_bot=False, first_name='admin')
user = User(id=1337, is_bot=False, first_name='user')


class TestMessage(Message):
    _current_id = 0

    def __init__(self, text: str, *, user: User = admin):
        message_id = 52
        date = datetime.datetime.now()
        chat = Chat(id=69, type='private')
        super().__init__(message_id=message_id, date=date, chat=chat, text=text, from_user=user)
        
    def answer(self, text, *, parse_mode=None, reply_markup=None) -> dict:
        return {
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup
        }
    
    def answer_document(self, document, *, caption = None, parse_mode = None, reply_markup = None) -> dict:
        return {
            'document': document,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup
        }
    
    def answer_photo(self, photo, *, caption = None, parse_mode = None, reply_markup = None) -> dict:
        return {
            'photo': photo,
            'caption': caption,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup
        }   

    @classmethod
    def __generate_id(cls):
        cls._current_id = cls._current_id + 1
        return cls.__current_id
