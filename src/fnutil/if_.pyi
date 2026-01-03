from __future__ import annotations
from typing import Callable

__all__ = [
    "If",
    "if_",
]

def if_[T](condition: bool, /) -> If[T]: ...

class If[T]:
    def __init__(self, condition: bool, /): ...
    def then(self, fn: Callable[[], T], /) -> If[T]: ...
    def else_(self, fn: Callable[[], T], /) -> T: ...
