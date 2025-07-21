import unittest

from handlers.schedule import schedule_handler
from .test_message import TestMessage


class ScheduleTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_schedule_handler(self):
        message = TestMessage('Расписание')
        answer = await schedule_handler(message)
        self.assertEqual(answer['text'].count('\n'), 80)
