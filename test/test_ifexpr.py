from unittest import TestCase
from functional import if_


class TestIfexpr(TestCase):
    def test_if_(self):
        res: int = if_(True).then(lambda: 1).else_(lambda: 2)
        self.assertEqual(res, 1)

        res: int = if_(False).then(lambda: 1).else_(lambda: 2)
        self.assertEqual(res, 2)
