from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING, Callable, cast

from fnutil.base import _ExprChainable


if TYPE_CHECKING:
    from fnutil import Expr


class _If[T](_ExprChainable):
    def __init__(self, condition: bool, /) -> None:
        super().__init__()

        self.main_condition: bool = condition
        self.conditions: list[tuple[bool, T | Callable[[], T], bool]] = []
        self.then_init: bool = False

    def then(
        self, fn_or_val: T | Callable[[], T], /, *, call: bool = False
    ) -> _If[T]:
        if self.then_init:
            raise RuntimeError("Then branch declared more than once.")

        self.conditions.append((self.main_condition, fn_or_val, call))
        self.then_init = True

        return self

    def elif_(
        self,
        condition: bool,
        fn_or_val: T | Callable[[], T],
        /,
        *,
        call: bool = False,
    ) -> _If[T]:
        if not self.then_init:
            raise RuntimeError("Declared elif branch before then branch.")

        self.conditions.append((condition, fn_or_val, call))
        return self

    def else_(
        self, fn_or_val: T | Callable[[], T], /, *, call: bool = False
    ) -> Expr[T]:
        if not self.then_init:
            raise RuntimeError("Missing then() before else_()")

        self.conditions.append((True, fn_or_val, call))

        try:
            for condition, value, should_call in self.conditions:
                if not condition:
                    continue

                if isinstance(value, FunctionType):
                    fn = cast(Callable[[], T], value)
                    return self._make_expr(val=fn())
                if should_call and callable(value):
                    fn = cast(Callable[[], T], value)
                    return self._make_expr(val=fn())
                return self._make_expr(val=cast(T, value))

            raise RuntimeError("No condition matched (should not happen)")

        except Exception as e:
            return self._make_expr(err=e)
