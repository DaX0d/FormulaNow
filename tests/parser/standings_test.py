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
    

    def test_get_drivers(self):
        drivers = parser.standings.get_drivers()
        self.assertIsInstance(drivers, dict)
        self.assertTrue(len(drivers.keys()) >= 20)
        self.assertTrue(all([len(key.split('(')) == 2 for key in drivers.keys()]))

    
    def test_get_teams(self):
        teams = parser.standings.get_teams()
        self.assertIsInstance(teams, dict)
        self.assertEqual(len(teams.keys()), 10)
