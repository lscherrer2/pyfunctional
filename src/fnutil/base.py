from __future__ import annotations

from typing import TYPE_CHECKING, cast, overload

if TYPE_CHECKING:
    from fnutil import Expr


class _ExprChainable:
    _Expr: type[Expr] | None = None

    def __init__(self):
        self._runtime_import()

    @classmethod
    def _runtime_import(cls):
        if cls._Expr is not None:
            return

        from fnutil import Expr

        cls._Expr = Expr

    @overload
    def _make_expr[V](self, *, val: V) -> Expr[V]: ...

    @overload
    def _make_expr[V](self, *, err: Exception) -> Expr[V]: ...

    def _make_expr[V](
        self, *, val: V | None = None, err: Exception | None = None
    ) -> Expr[V]:
        from typing import cast as _cast
        from fnutil import Expr as _Expr_type

        assert self._Expr is not None
        if val is not None:
            return _cast(_Expr_type[V], self._Expr(val=val))
        if err is not None:
            return _cast(_Expr_type[V], self._Expr(err=err))
        raise ValueError("Must provide either val or err")
