from unittest import TestCase

import fnutil as fn


class TestExpr(TestCase):
    def test_map(self):
        result = fn.expr(2).map(lambda x: x + 1)
        self.assertEqual(result.val, 3)

    def test_map_chains(self):
        result = fn.expr(5).map(lambda x: x * 2).map(lambda x: x + 1)
        self.assertEqual(result.val, 11)

    def test_map_catches_exceptions(self):
        result = fn.expr(0).map(lambda x: 1 // x)
        self.assertTrue(result.is_err)
        self.assertIsInstance(result.err, ZeroDivisionError)

    def test_map_err(self):
        result = (
            fn.expr(0).map(lambda x: 1 // x).map_err(lambda e: "recovered")
        )
        self.assertEqual(result.val, "recovered")

    def test_unwrap_success(self):
        result = fn.expr(42).unwrap()
        self.assertEqual(result, 42)

    def test_unwrap_raises(self):
        with self.assertRaises(ValueError):
            fn.expr(1).map(
                lambda x: (_ for _ in ()).throw(ValueError("test"))
            ).unwrap()

    def test_if_then_else(self):
        result = fn.expr(True).if_().then(100).else_(200)
        self.assertEqual(result.val, 100)

        result = fn.expr(False).if_().then(100).else_(200)
        self.assertEqual(result.val, 200)

    def test_if_with_functions(self):
        result = fn.expr(True).if_().then(lambda: "yes").else_(lambda: "no")
        self.assertEqual(result.val, "yes")

        result = fn.expr(0).if_().then(lambda: "yes").else_(lambda: "no")
        self.assertEqual(result.val, "no")

    def test_match(self):
        result = fn.expr(42).match().case(int, "number").evaluate()
        self.assertEqual(result.val, "number")

    def test_match_with_lambda(self):
        result = fn.expr(5).match().case(int, lambda x: x * 2).evaluate()
        self.assertEqual(result.val, 10)

    def test_chaining(self):
        result = (
            fn.expr(5)
            .map(lambda x: x * 2)
            .match()
            .case(10, "ten")
            .evaluate()
            .if_()
            .then("success")
            .else_("failed")
        )
        self.assertEqual(result.val, "success")
