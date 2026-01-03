from __future__ import annotations
from collections.abc import Iterable
from fnutil.iterator import iterate, Iterator
from fnutil.match import match_type, match_value, MatchValue, MatchType
from fnutil.if_ import if_, If
from typing import Callable


class Expr[T]:
    def __init__(self, value: T, /, err: bool = False):
        self.value: T = value
        self.err: bool = err

    def match_type[V](self) -> MatchType[T, V]:
        return match_type(self.value)

    def match_value[V](self) -> MatchValue[T, V]:
        return match_value(self.value)

    def if_[V](self, fn: Callable[[], V]) -> If[V]:
        return if_(bool(self.value)).then(fn)

    def iterate[U](self: Expr[Iterable[U]]) -> Iterator[U]:
        return iterate(self.value)

    def map_value[V](self, fn: Callable[[T], V]) -> Expr[V]:
        return Expr(fn(self.value))

    def try_map_value[V](self, fn: Callable[[T], V]) -> Expr[V | Exception]:
        try:
            return Expr(fn(self.value))
        except Exception as e:
            return Expr(e, err=True)

    def catch[E, V](self, exception: type[E], fn: Callable[[E], V]) -> Expr[T | V]:
        if not self.err or not isinstance(self.value, exception):
            return self

        return Expr(fn(self.value))


def expr[T](value: T, /) -> Expr[T]:
    return Expr(value)
