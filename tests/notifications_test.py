import unittest
from datetime import datetime

from notifications import Conditions, MOSCOW_TZ
from utils import try_open


class NotificationsTeasCase(unittest.TestCase):
    @unittest.skipUnless(
        try_open('parser/data/standings.json'),
        'file does not exist'
    )
    def test_qualy_condition(self):
        conditions = Conditions()
        self.assertFalse(conditions.is_qualy_soon())
        self.assertTrue(conditions.is_qualy_soon(datetime(
            2025, 7, 26, 16, 10, tzinfo=MOSCOW_TZ
        )))
    
    @unittest.skipUnless(
        try_open('parser/data/standings.json'),
        'file does not exist'
    )
    def test_race_tomorrow(self):
        conditions = Conditions()
        self.assertFalse(conditions.is_race_tomorrow())
        self.assertTrue(conditions.is_race_tomorrow(datetime(
            2025, 7, 26, 20, 21, tzinfo=MOSCOW_TZ
        )))
    
    @unittest.skipUnless(
        try_open('parser/data/standings.json'),
        'file does not exist'
    )
    def test_race_soon(self):
        conditions = Conditions()
        self.assertFalse(conditions.is_race_soon())
        self.assertTrue(conditions.is_race_soon(datetime(
            2025, 7, 27, 15, 30, tzinfo=MOSCOW_TZ
        )))
