from __future__ import annotations
from typing import Callable


def match[T, V](value: T) -> Match[T, V]:
    return Match[T, V](value)


class Match[T, V]:
    def __init__(self, value: T):
        self.value: T = value
        self.cases: list[tuple[T | type[T], Callable[[T], V]]] = []
        self.default_case: Callable[[T], V] | None = None

    def case(self, value: T | type[T], closure: Callable[[T], V], /) -> Match[T, V]:
        self.cases.append((value, closure))
        return self

    def default(self, closure: Callable[[T], V], /) -> V:
        if self.default_case is not None:
            raise RuntimeError("Received multiple defaults")
        self.default_case = closure
        return self.evaluate()

    def evaluate(self) -> V:
        for v, f in self.cases:
            if self.value == v:
                return f(self.value)

        for v, f in self.cases:
            if type(self.value) is v:
                return f(self.value)

        if self.default_case:
            return self.default_case(self.value)

        raise ValueError("No Matching Arm")
