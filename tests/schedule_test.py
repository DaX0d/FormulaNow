import unittest
import requests

import parser


class ScheduleTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_parse_chedule(self):
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_schedule
        )

    def test_get_schedule(self):
        schedule = parser.schedule.get_schedule()
        self.assertIsInstance(schedule, dict)
        self.assertIsInstance(schedule['id'], int)
        self.assertIsInstance(schedule['name'], str)
        self.assertIsInstance(schedule['date'], str)
        self.assertIsInstance(schedule['race_time'], str)
        self.assertIsInstance(schedule['q_time'], str)
