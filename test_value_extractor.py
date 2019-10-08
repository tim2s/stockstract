from unittest import TestCase

from value_extractor import parse_german_float


class TestParseValueExtractor(TestCase):

  def test_parse_german_float(self):
    string = '2.629,00'

    self.assertEqual(parse_german_float(string), float(2629))

  def test_minus(self):
    string = '-'

    self.assertEqual(parse_german_float(string), float(0))
