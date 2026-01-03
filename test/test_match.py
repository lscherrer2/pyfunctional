from unittest import TestCase
from functional import match


class TestMatch(TestCase):
    def test_default(self):
        res = match(7.2).case(int, lambda x: 100.0).default(lambda x: 0.0)
        self.assertEqual(res, 0.0)

    def test_match_value(self):
        res = (
            match(1)
            .case(1, lambda x: x + 9)
            .case(3, lambda x: x + 7)
            .case(5, lambda x: x + 5)
            .default(lambda x: x)
        )
        self.assertEqual(res, 10)
        res = (
            match(3)
            .case(1, lambda x: x + 9)
            .case(3, lambda x: x + 7)
            .case(5, lambda x: x + 5)
            .default(lambda x: x)
        )
        self.assertEqual(res, 10)
        res = (
            match(5)
            .case(1, lambda x: x + 9)
            .case(3, lambda x: x + 7)
            .case(5, lambda x: x + 5)
            .default(lambda x: x)
        )
        self.assertEqual(res, 10)
        res = (
            match(50)
            .case(1, lambda x: x + 9)
            .case(3, lambda x: x + 7)
            .case(5, lambda x: x + 5)
            .case(7, lambda x: x + 3)
            .default(lambda x: x)
        )
        self.assertEqual(res, 50)

    def test_match_type(self):
        res = (
            match(1.0)
            .case(float, lambda _: float)
            .case(int, lambda _: int)
            .default(lambda _: bool)
        )
        self.assertIs(res, float)
        res = (
            match(1)
            .case(float, lambda _: float)
            .case(int, lambda _: int)
            .default(lambda _: bool)
        )
        self.assertIs(res, int)
        res = (
            match(type)
            .case(float, lambda _: float)
            .case(int, lambda _: int)
            .default(lambda _: bool)
        )
        self.assertIs(res, bool)
