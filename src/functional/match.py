from __future__ import annotations
from typing import Callable, Any
from typeguard import check_type, TypeCheckError
from types import FunctionType


def match_value[T, V](value: T) -> MatchValue[T, V]:
    return MatchValue(value)


def match_type[T, V](value: T) -> MatchType[T, V]:
    return MatchType(value)


class MatchValue[T, V]:
    def __init__(self, value: T, /):
        self.value: T = value
        self.cases: list[tuple[T, Callable[[T], V] | V]] = []
        self.default_case: Callable[[T], V] | V | None = None

    def case(self, value: T, fn_or_value: Callable[[T], V] | V, /) -> MatchValue[T, V]:
        self.cases.append((value, fn_or_value))
        return self

    def default(self, fn_or_value: Callable[[T], V] | V, /) -> MatchValue[T, V]:
        if self.default_case is not None:
            raise RuntimeError("Received multiple defaults")

        self.default_case = fn_or_value
        return self

    def evaluate(self) -> V:
        for value, fn_or_value in self.cases:
            if self.value == value:
                if isinstance(fn_or_value, FunctionType):
                    return fn_or_value(self.value)

                return fn_or_value

        if fn_or_value := self.default_case:
            if isinstance(fn_or_value, FunctionType):
                return fn_or_value(self.value)

            return fn_or_value

        raise ValueError("No Matching Arm")


def _is_type(value: Any, annotation: type):
    try:
        check_type(value, annotation)
        return True
    except TypeCheckError:
        return False


class MatchType[T, V]:
    def __init__(self, value: T):
        self.value: T = value
        self.cases: list[tuple[type, Callable[[T], V] | V]] = []
        self.default_case: Callable[[T], V] | V | None = None

    def case(
        self, annotation: type, fn_or_value: Callable[[T], V] | V, /
    ) -> MatchType[T, V]:
        self.cases.append((annotation, fn_or_value))
        return self

    def default(self, fn_or_value: Callable[[T], V] | V, /) -> MatchType[T, V]:
        if self.default_case is not None:
            raise RuntimeError("Received multiple defaults")

        self.default_case = fn_or_value
        return self

    def evaluate(self) -> V:
        for annotation, fn_or_value in self.cases:
            if _is_type(self.value, annotation):
                if isinstance(fn_or_value, FunctionType):
                    return fn_or_value(self.value)

                return fn_or_value

        if fn_or_value := self.default_case:
            if isinstance(fn_or_value, FunctionType):
                return fn_or_value(self.value)

            return fn_or_value

        raise ValueError("No Matching Arm")
