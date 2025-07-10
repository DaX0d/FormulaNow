import unittest

import parser


class ParserMainTestCase(unittest.TestCase):
    def test_parse_all(self):
        with self.assertLogs('root', level='WARNING') as cm:
            parser.parse_all()
