from __future__ import annotations
from typing import Callable
from types import FunctionType


def match[T, V](value: T) -> Match[T, V]:
    return Match[T, V](value)


class Match[T, V]:
    def __init__(self, value: T):
        self.value: T = value
        self.cases: list[tuple[T | type[T], Callable[[T], V] | V]] = []
        self.default_case: Callable[[T], V] | V | None = None

    def case(
        self, value: T | type[T], fn_or_value: Callable[[T], V] | V, /
    ) -> Match[T, V]:
        self.cases.append((value, fn_or_value))
        return self

    def default(self, fn_or_value: Callable[[T], V] | V, /) -> V:
        if self.default_case is not None:
            raise RuntimeError("Received multiple defaults")
        self.default_case = fn_or_value
        return self.evaluate()

    def evaluate(self) -> V:
        for v, f in self.cases:
            if self.value == v:
                if isinstance(f, FunctionType):
                    return f(self.value)
                else:
                    return f

        for v, f in self.cases:
            if type(self.value) is v:
                if isinstance(f, FunctionType):
                    return f(self.value)
                else:
                    return f

        if f := self.default_case:
            if isinstance(f, FunctionType):
                return f(self.value)
            else:
                return f

        raise ValueError("No Matching Arm")
