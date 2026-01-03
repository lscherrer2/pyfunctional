from unittest import TestCase

import fnutil as fn


class TestMatch(TestCase):
    def test_match_type(self):
        res = (
            fn.expr(False)
            .match_type()
            .case(int, lambda x: "int")
            .default(lambda x: None)
            .evaluate()
        )
        self.assertEqual(res, "int")

        res = (
            fn.expr(8)
            .match_type()
            .case(bool, lambda x: "bool")
            .case(int | float, lambda x: "number")
            .default(lambda x: "default")
            .evaluate()
        )
        self.assertEqual(res, "number")

    def test_match_type_bool_is_caught_by_int_if_int_case_first(self):
        res = (
            fn.expr(True)
            .match_type()
            .case(int, "int")
            .case(bool, "bool")
            .default("default")
            .evaluate()
        )
        self.assertEqual(res, "int")

        res = (
            fn.expr(True)
            .match_type()
            .case(bool, "bool")
            .case(int, "int")
            .default("default")
            .evaluate()
        )
        self.assertEqual(res, "bool")

    def test_match_type_errors(self):
        with self.assertRaises(RuntimeError):
            fn.expr(1).match_type().default("a").default("b")

        with self.assertRaises(ValueError):
            fn.expr("x").match_type().case(int, "int").evaluate()

    def test_match_value(self):
        res = (
            fn.expr(False)
            .match_value()
            .case(True, lambda x: "true")
            .case(False, lambda x: "false")
            .default(lambda x: "default")
            .evaluate()
        )
        self.assertEqual(res, "false")

        res = (
            fn.expr(8)
            .match_value()
            .case(True, lambda x: "true")
            .case(False, lambda x: "false")
            .default(lambda x: "default")
            .evaluate()
        )
        self.assertEqual(res, "default")

        res = (
            fn.expr(8)
            .match_value()
            .case(True, lambda x: "true")
            .case(8, lambda x: "number")
            .default(lambda x: "default")
            .evaluate()
        )
        self.assertEqual(res, "number")

    def test_match_value_errors_and_constants(self):
        res = fn.expr(1).match_value().case(1, "one").default("default").evaluate()
        self.assertEqual(res, "one")

        with self.assertRaises(RuntimeError):
            fn.expr(1).match_value().default("a").default("b")

        with self.assertRaises(ValueError):
            fn.expr(1).match_value().case(2, "two").evaluate()
