from __future__ import annotations
from typing import Callable


class _If[T]:
    def __init__(self, condition: bool, /) -> None:
        self.result: T
        self.then_fn: Callable[[], T]
        self.condition: bool = condition

    def then(self, fn: Callable[[], T], /) -> _If[T]:
        self.then_fn = fn
        return self

    def else_(self, fn: Callable[[], T], /) -> T:
        if self.condition:
            return self.then_fn()

        return fn()


def if_[T](condition: bool, /) -> _If[T]:
    return _If[T](condition)


__all__ = ["if_"]
