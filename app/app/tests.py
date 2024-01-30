"""
Sample tests
"""

from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):
    """ Test the class module """

    def test_add_number(self):
        """test adding numbers together."""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_number(self):
        """test subtract numbers together."""
        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)
