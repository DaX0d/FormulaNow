import unittest
from sys import stdout

import parser


class ParserMainTestCase(unittest.TestCase):
    def test_parse_all(self):
        with self.assertNoLogs('root', level='WARNING') as cm:
            parser.parse_all()
