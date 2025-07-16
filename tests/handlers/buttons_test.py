import unittest

from handlers.buttons import buttons_handler
import settings
from .test_message import TestMessage
from markups import results_markup
from utils import try_open


class ButtonsTestCase(unittest.IsolatedAsyncioTestCase):
    @unittest.skipUnless(
        try_open('parser/data/schedule.json'),
        'file does not exist')
    async def test_schedule_button(self):
        message = TestMessage('Расписание заездов')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'].split('\n')[0], settings.schedule_ans.replace('\n', ''))

    @unittest.skipUnless(
        try_open('parser/data/schedule.json'),
        'file does not exist')
    async def test_next_race_button(self):
        message = TestMessage('Следующая гонка')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'].split('\n')[0], settings.next_race_ans.replace('\n', ''))
    
    @unittest.skipUnless(
        try_open('parser/data/schedule.json'),
        'file does not exist')
    async def test_track_button(self):
        message = TestMessage('Трасса')
        answer = await buttons_handler(message)
        self.assertEqual(len(answer['caption'].split('\n')), 7)

    @unittest.skipUnless(
        try_open('parser/data/standings.json'),
        'file does not exist')
    async def test_standings_button(self):
        message = TestMessage('Личный зачет')
        answer = await buttons_handler(message)
        self.assertEqual(
            answer['text'].split('\n')[0],
            settings.standings_ans.split('\n')[0]
        )

    @unittest.skipUnless(
        try_open('parser/data/standings.json'),
        'file does not exist')
    async def test_teams_handler(self):
        message = TestMessage('Кубок конструкторов')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'].split('\n')[0], settings.teams_ans.replace('\n', ''))

    @unittest.skipUnless(
        try_open('parser/data/last.json'),
        'file does not exist')
    async def test_results_button(self):
        message = TestMessage('Результаты последней гонки')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'], settings.results_ans)
        self.assertEqual(answer['reply_markup'], results_markup)

    @unittest.skipUnless(
        try_open('parser/data/last.json'),
        'file does not exist')
    async def test_last_race_button(self):
        message = TestMessage('Гонка')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'].split('\n')[0], settings.last_race_ans.replace('\n', ''))

    @unittest.skipUnless(
        try_open('parser/data/last.json'),
        'file does not exist')
    async def test_last_qualy_button(self):
        message = TestMessage('Квалификация')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'].split('\n')[0], settings.last_qualy_ans.replace('\n', ''))

    async def test_list_of_users_button(self):
        message = TestMessage('Список пользователей')
        answer = await buttons_handler(message)
        self.assertTrue(answer['document'])

    async def test_number_of_users_button(self):
        message = TestMessage('Количество пользователей')
        answer = await buttons_handler(message)
        self.assertTrue(answer['text'].isdigit())
    
    async def test_parser_data_button(self):
        message = TestMessage('Данные парсера')
        answer = await buttons_handler(message)
        self.assertTrue(answer['document'])
    
    async def test_parser_reload_button(self):
        message = TestMessage('Перезапуск парсера')
        answer = await buttons_handler(message)
        self.assertEqual(answer['text'], 'Парсер перезапущен')
    
    # async def test_reload_notifications(self):
    #     message = TestMessage('Перезапуск уведомлений')
    #     answer = await buttons_handler(message)
    #     self.assertEqual(answer['text'], 'Уведомления перезапущены')
