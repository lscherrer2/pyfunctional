from unittest import TestCase
from functional import if_


class TestIfexpr(TestCase):
    def test_if_(self):
        res: int = if_(True).then(lambda: 1).else_(lambda: 2)
        self.assertEqual(res, 1)

        res: int = if_(False).then(lambda: 1).else_(lambda: 2)
        self.assertEqual(res, 2)

    def test_else_without_then_raises(self):
        with self.assertRaises(RuntimeError):
            _ = if_(True).else_(lambda: 1)
