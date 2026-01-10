from __future__ import annotations

from types import FunctionType, UnionType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Union,
    cast,
    get_origin,
)

from typeguard import check_type

from fnutil.base import _ExprChainable


if TYPE_CHECKING:
    from fnutil import Expr


class MatchError(Exception):
    pass


class _Case[T, V]:
    def __init__(
        self, cmp: Any, fn_or_val: V | Callable[[T], V], call: bool = False
    ):
        self.cmp = cmp
        self.fn_or_val = fn_or_val
        self.call = call

    def match(self, other: T) -> bool:
        is_type = isinstance(self.cmp, type)
        is_union = (
            isinstance(self.cmp, UnionType) or get_origin(self.cmp) is Union
        )

        if is_type or is_union:
            try:
                check_type(other, self.cmp)
                return True
            except Exception:
                return False

        return self.cmp is other or self.cmp == other

    def evaluate(self, val: T) -> V:
        if isinstance(self.fn_or_val, FunctionType):
            fn = cast(Callable[[T], V], self.fn_or_val)
            return fn(val)
        if self.call and callable(self.fn_or_val):
            fn = cast(Callable[[T], V], self.fn_or_val)
            return fn(val)
        return cast(V, self.fn_or_val)


class _Match[T, V](_ExprChainable):
    def __init__(self, val: T):
        super().__init__()

        self.val: T = val
        self.cases: list[_Case[T, V]] = []
        self._default: tuple[V | Callable[[T], V], bool] | None = None

    def case(
        self, cmp: Any, fn_or_val: V | Callable[[T], V], *, call: bool = False
    ) -> _Match[T, V]:
        self.cases.append(_Case(cmp=cmp, fn_or_val=fn_or_val, call=call))
        return self

    def default(
        self, v: V | Callable[[T], V], *, call: bool = False
    ) -> _Match[T, V]:
        if self._default is not None:
            raise RuntimeError("Default case already defined")
        self._default = (v, call)
        return self

    def evaluate(self) -> Expr[V]:
        for case in self.cases:
            if case.match(self.val):
                try:
                    result = case.evaluate(self.val)
                    return self._make_expr(val=result)
                except Exception as e:
                    return self._make_expr(err=e)

        if self._default is None:
            msg = f"No case matched value {self.val} and no default provided"
            raise ValueError(msg)

        default_val, call = self._default

        try:
            if isinstance(default_val, FunctionType):
                fn = cast(Callable[[T], V], default_val)
                return self._make_expr(val=fn(self.val))
            if call and callable(default_val):
                fn = cast(Callable[[T], V], default_val)
                return self._make_expr(val=fn(self.val))
            return self._make_expr(val=cast(V, default_val))
        except Exception as e:
            return self._make_expr(err=e)
