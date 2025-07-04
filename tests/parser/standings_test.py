import unittest
import requests
import json

from utils import try_open
import parser


class StandingsTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_parse_drivers(self):
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.standings.parse_drivers
        )


    @unittest.expectedFailure
    def test_parse_teams(self):
        self.assertRaises(
            requests.exceptions.ConnectionError,
            parser.standings.parse_teams
        )
    

    @unittest.skipUnless(
        try_open('parser/data/standings.json'),
        'file does not exist'
    )
    def test_standings_json(self):
        with open('parser/data/standings.json', 'r', encoding='utf-8') as file:
            json_data: dict = json.load(file)
            self.assertTrue('drivers' in json_data.keys())
            self.assertTrue('teams' in json_data.keys())
    