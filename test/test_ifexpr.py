from unittest import TestCase

import fnutil as fn


class TestIfexpr(TestCase):
    def test_if_(self):
        res = fn.expr(True).if_().then(lambda: 1).else_(lambda: 2)
        self.assertEqual(res.val, 1)

        res = fn.expr(False).if_().then(lambda: 1).else_(lambda: 2)
        self.assertEqual(res.val, 2)

    def test_else_without_then_raises(self):
        with self.assertRaises(RuntimeError):
            _ = fn.expr(True).if_().else_(lambda: 1)
