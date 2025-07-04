import unittest
import requests
import json

import parser
from utils import try_open


class ScheduleTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_parse_chedule(self):
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_schedule
        )


    @unittest.expectedFailure
    def test_parse_last_race(self):
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_last_race
        )


    @unittest.skipUnless(
        try_open('parser/data/last.json'),
        'file does not exist'
    )
    def test_last_json(self):
        with open('parser/data/last.json', 'r', encoding='utf-8') as file:
            last_race: dict = json.load(file)
            self.assertTrue('race' in last_race.keys())
            self.assertTrue('qualy' in last_race.keys())


    @unittest.skipUnless(
        try_open('parser/data/schedule.json'),
        'file does not exist'
    )
    def test_get_schedule(self):
        schedule = parser.schedule.get_schedule()
        self.assertIsInstance(schedule, dict)
        self.assertIsInstance(schedule['id'], int)
        self.assertIsInstance(schedule['name'], str)
        self.assertIsInstance(schedule['date'], str)
        self.assertIsInstance(schedule['race_time'], str)
        self.assertIsInstance(schedule['q_time'], str)


    @unittest.skipUnless(
        try_open('parser/data/schedule.json'),
        'file does not exist'
    )
    def test_next_race(self):
        next_race = parser.schedule.get_next_race()
        self.assertIsInstance(next_race, dict)
        self.assertIsInstance(next_race['name'], str)
        self.assertIsInstance(next_race['race_date'], str)
        self.assertIsInstance(next_race['track'], dict)
        self.assertIsInstance(next_race['schedule'], dict)
        self.assertIsInstance(next_race['gp'], dict)


    @unittest.skipUnless(
        try_open('parser/data/last.json'),
        'file does not exist'
    )
    def test_last_race(self):
        last_race = parser.schedule.get_last_race()
        self.assertIsInstance(last_race, dict)
        self.assertEqual(len(last_race['races']['results']), 20)
    

    @unittest.skipUnless(
        try_open('parser/data/last.json'),
        'file does not exist'
    )
    def test_last_qualy(self):
        last_qualy = parser.schedule.get_last_qualy()
        self.assertIsInstance(last_qualy, dict)
        self.assertEqual(len(last_qualy['races']['qualyResults']), 20)
