from __future__ import annotations

from typing import Any, Callable

from fnutil.expr import Expr

class _Match[T, V]:
    def case(
        self,
        cmp: Any,
        fn_or_val: Callable[[T], V] | V,
        /,
        *,
        call: bool = False,
    ) -> _Match[T, V]: ...
    def default(
        self, fn_or_val: Callable[[T], V] | V, /, *, call: bool = False
    ) -> _Match[T, V]: ...
    def evaluate(self) -> Expr[V]: ...
