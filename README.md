## FnUtil

Lightweight functional-style helpers for Python 3.13+.

This package focuses on a small set of composable building blocks:

- `expr(...)`: an expression wrapper that enables chaining.
- `match_value(...)` / `match_type(...)`: fluent “match” builders.
- `iterate(...)`: a lazy iterator wrapper with common helpers.

All examples in this README use:

```py
import fnutil as fn
```

## `expr` and chaining

`fn.expr(x)` wraps a value and keeps it in `.value`.

```py
import fnutil as fn

assert fn.expr(2).map_value(lambda x: x + 1).value == 3
```

### Safe mapping + recovery

`try_map_value` catches exceptions and stores them as the wrapped value; `catch` can then recover.

```py
import fnutil as fn

result = (
	fn.expr(0)
	.try_map_value(lambda x: 10 // x)
	.catch(ZeroDivisionError, lambda e: 0)
)

assert result.value == 0
```

### Conditional expressions

`Expr.if_` uses truthiness of the wrapped value.

```py
import fnutil as fn

assert fn.expr(True).if_(lambda: "yes").else_(lambda: "no") == "yes"
assert fn.expr(0).if_(lambda: "yes").else_(lambda: "no") == "no"
```

## Matching

Matching is a two-step process:

1. Build cases with `.case(...)` (and optionally `.default(...)`)
2. Call `.evaluate()`

### Match by value

```py
import fnutil as fn

out = (
	fn.expr("b")
	.match_value()
	.case("a", "A")
	.case("b", "B")
	.default("?")
	.evaluate()
)

assert out == "B"
```

### Match by type

```py
import fnutil as fn

out = (
	fn.expr(8)
	.match_type()
	.case(int | float, "number")
	.default("other")
	.evaluate()
)

assert out == "number"
```

#### Note on `bool` vs `int`

In Python, `bool` is a subclass of `int`, so type matching follows the *order of cases*.
If you put `int` first, `True`/`False` will match the `int` arm (this is intended behavior).

```py
import fnutil as fn

assert (
	fn.expr(True)
	.match_type()
	.case(int, "int")
	.case(bool, "bool")
	.evaluate()
) == "int"

assert (
	fn.expr(True)
	.match_type()
	.case(bool, "bool")
	.case(int, "int")
	.evaluate()
) == "bool"
```

## Iterator utilities

`Iterator[T]` is a lazy wrapper: operations like `map` and `filter` create new iterators.

When you start from an `expr`, you can go directly into iterator mode via `.iterate()`.

```py
import fnutil as fn

xs = fn.expr([1, 2, 3, 4]).iterate()

evens = xs.filterfalse(lambda x: x % 2)
assert list(evens) == [2, 4]

doubled = fn.expr([1, 2, 3]).iterate().map(lambda x: x * 2)
assert list(doubled) == [2, 4, 6]

flat = fn.expr([[1, 2], [], [3]]).iterate().flatten()
assert list(flat) == [1, 2, 3]
```

Common convenience methods include: `collect`, `chain`, `zip`, `enumerate`, `fold`, `reduce`,
`sum`, `min`, `max`, and slicing via `it[start:stop:step]`.

## Direct usage (not recommended)

You *can* use the lower-level helpers directly (e.g. `fn.if_`, `fn.iterate`, `fn.match_type`,
`fn.match_value`) but the intended usage is to start from `fn.expr(...)` and chain from there.
