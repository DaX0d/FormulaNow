import unittest

import parser


class ParserMainTestCase(unittest.TestCase):
    def test_parse_all(self):
        parser.parse_all()
        self.assertTrue(True)
