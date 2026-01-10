from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast, overload

if TYPE_CHECKING:
    from fnutil.match import _Match
    from fnutil.if_ import _If


class Expr[T]:
    @overload
    def __init__(self, *, val: T) -> None: ...

    @overload
    def __init__(self, *, err: Exception) -> None: ...

    def __init__(self, *, val: T | None = None, err: Exception | None = None):
        if val is not None and err is not None:
            raise ValueError("Cannot provide both 'val' and 'err'")
        if val is None and err is None:
            raise ValueError("Must provide either 'val' or 'err'")

        self._is_err = err is not None
        if self._is_err:
            self.inner: T | Exception = cast(Exception, err)
        else:
            self.inner = cast(T, val)

    @property
    def is_err(self) -> bool:
        return self._is_err

    @property
    def is_val(self) -> bool:
        return not self._is_err

    @property
    def err(self) -> Exception | None:
        if self._is_err:
            return cast(Exception, self.inner)
        return None

    @property
    def val(self) -> T | None:
        if not self._is_err:
            return cast(T, self.inner)
        return None

    def unwrap(self) -> T:
        if self._is_err:
            raise cast(Exception, self.inner)
        return cast(T, self.inner)

    def map[V](self, fn: Callable[[T], V]) -> Expr[V]:
        if self._is_err:
            return Expr(err=cast(Exception, self.inner))

        try:
            return Expr(val=fn(cast(T, self.inner)))
        except Exception as e:
            return Expr(err=e)

    def map_err[V](self, fn: Callable[[Exception], V]) -> Expr[V]:
        if not self._is_err:
            return Expr(val=cast(V, self.inner))

        try:
            return Expr(val=fn(cast(Exception, self.inner)))
        except Exception as e:
            return Expr(err=e)

    def match[V](self) -> _Match[T, V]:
        from fnutil.match import _Match

        if self._is_err:
            raise cast(Exception, self.inner)
        return _Match(cast(T, self.inner))

    def if_[V](self) -> _If[V]:
        from fnutil.if_ import _If

        if self._is_err:
            raise cast(Exception, self.inner)

        condition = bool(cast(T, self.inner))
        return _If(condition)

    @classmethod
    def _wrap(cls, val: T | Exception):
        if isinstance(val, Exception):
            return cls(err=val)
        return cls(val=val)


def expr[T](value: T, /) -> Expr[T]:
    return Expr(val=value)
