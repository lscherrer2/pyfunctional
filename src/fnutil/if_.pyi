from __future__ import annotations

from typing import Callable

from fnutil.expr import Expr

class _If[T]:
    def then(
        self, fn_or_val: Callable[[], T] | T, /, *, call: bool = False
    ) -> _If[T]: ...
    def elif_(
        self,
        condition: bool,
        fn_or_val: Callable[[], T] | T,
        /,
        *,
        call: bool = False,
    ) -> _If[T]: ...
    def else_(
        self, fn_or_val: Callable[[], T] | T, /, *, call: bool = False
    ) -> Expr[T]: ...
