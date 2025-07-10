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
        if parser.schedule.parse_last_race() == 404:
            self.skipTest('404')
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_last_race
        )
    

    @unittest.expectedFailure
    def test_pasre_last_qualy(self):
        if parser.schedule.parse_last_qualy() == 404:
            self.skipTest('404')
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_last_qualy
        )


    @unittest.expectedFailure
    def test_parse_last_sprint(self):
        if parser.schedule.parse_last_sprint() == 404:
            self.skipTest('404')
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_last_sprint
        )

    
    @unittest.expectedFailure
    def test_parse_last_sprint_qualy(self):
        if parser.schedule.parse_last_sprint_qualy() == 404:
            self.skipTest('404')
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.schedule.parse_last_sprint_qualy
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
        self.assertIsInstance(schedule, list)
        self.assertIsInstance(schedule[0]['id'], int)
        self.assertIsInstance(schedule[0]['name'], str)
        self.assertIsInstance(schedule[0]['date'], str)
        self.assertIsInstance(schedule[0]['race_time'], str)
        self.assertIsInstance(schedule[0]['q_time'], str)


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
