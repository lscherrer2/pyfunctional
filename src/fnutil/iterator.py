from __future__ import annotations

from functools import reduce
from itertools import chain, filterfalse, islice
import typing
from typing import Any, Callable, Iterable, overload


__all__ = [
    "Iterator",
    "iterate",
]


def iterate[T](iterable: Iterable[T], /) -> Iterator[T]:
    return Iterator(iterable)


class Iterator[T]:
    def __init__(self, inner: Iterable[T]):
        self.inner: Iterable[T] = inner

    def __iter__(self) -> typing.Iterator[T]:
        return iter(self.inner)

    def filter(self, fn: Callable[[T], bool]) -> Iterator[T]:
        return self._wrap(filter(fn, self))

    def filterfalse(self, fn: Callable[[T], bool]) -> Iterator[T]:
        return self._wrap(filterfalse(fn, self))

    def map[U](self, fn: Callable[[T], U]) -> Iterator[U]:
        return self._wrap(map(fn, self))

    def filter_map[U](self, fn: Callable[[T], U | None]) -> Iterator[U]:
        def gen():
            for item in self:
                v = fn(item)
                if v is not None:
                    yield v

        return self._wrap(gen())

    def for_each(self, fn: Callable[[T], Any]) -> None:
        for item in self:
            fn(item)

    def try_for_each(self, fn: Callable[[T], Any]) -> None:
        for item in self:
            try:
                fn(item)
            except Exception:
                continue

    def chain(self, *others: Iterable[T]) -> Iterator[T]:
        return self._wrap(chain(self, *others))

    def enumerate(self) -> Iterator[tuple[int, T]]:
        return self._wrap(enumerate(self))

    def zip[U](self, other: Iterable[U]) -> Iterator[tuple[T, U]]:
        return self._wrap(zip(self, other))

    def flatten[U](self: Iterator[Iterable[U]]) -> Iterator[U]:
        def gen():
            for it in self:
                for x in it:
                    yield x

        return self._wrap(gen())

    def collect[U](self, cls: type[U]) -> U:
        return cls(self)

    def sum(self) -> T:
        return sum(self)

    def min(self) -> T:
        return min(self)

    def max(self) -> T:
        return max(self)

    def fold[U](self, fn: Callable[[U, T], U], initial: U) -> U:
        return (
            reduce(fn, self, initial)
            if initial is not None
            else reduce(fn, self)
        )

    @overload
    def reduce(self, fn: Callable[[T, T], T], initial: None = None) -> T: ...

    @overload
    def reduce[U](self, fn: Callable[[U, T], U], initial: U) -> U: ...

    def reduce(self, fn, initial=None):
        return (
            reduce(fn, self, initial)
            if initial is not None
            else reduce(fn, self)
        )

    def __getitem__(self, i: slice) -> Iterator[T]:
        if not isinstance(i, slice):
            raise TypeError(
                "Iterator.__getitem__ can only receive a slice object"
            )
        return self._wrap(islice(self, i.start, i.stop, i.step))

    @classmethod
    def _wrap(cls, inner: Iterable[T]) -> Iterator[T]:
        return cls(inner=inner)
