from unittest import TestCase

import fnutil as fn


class TestExpr(TestCase):
    def test_map_value(self):
        self.assertEqual(fn.expr(2).map_value(lambda x: x + 1).value, 3)

    def test_try_map_value_success(self):
        out = fn.expr(2).try_map_value(lambda x: x * 2)
        self.assertEqual(out.value, 4)

    def test_try_map_value_exception_and_catch(self):
        out = fn.expr(0).try_map_value(lambda x: 1 // x)
        self.assertIsInstance(out.value, Exception)

        recovered = out.catch(ZeroDivisionError, lambda e: "recovered")
        self.assertEqual(recovered.value, "recovered")

    def test_if_iterate(self):
        res = fn.expr(True).if_(lambda: 1).else_(lambda: 2)
        self.assertEqual(res, 1)

        res = fn.expr(0).if_(lambda: 1).else_(lambda: 2)
        self.assertEqual(res, 2)

        self.assertEqual(list(fn.expr([1, 2, 3]).iterate()), [1, 2, 3])
