## FnUtil

Lightweight functional-style helpers for Python 3.13+.

When you use `fnutil`, you commit to **functional-style programming** - everything stays within the `Expr` monad until you explicitly unwrap.

## Installation

```bash
pip install fnutil
```

Or with uv:

```bash
uv add fnutil
```

## Usage

All examples use:

```py
import fnutil as fn
```

## The `Expr` Monad

`fn.expr(x)` wraps a value in the `Expr` monad. Access the wrapped value with `.val` or `.unwrap()`.

```py
result = fn.expr(2).map(lambda x: x + 1)
assert result.val == 3
```

### Core Expr Methods

- `.map(fn)` - Transform the value (catches exceptions)
- `.map_err(fn)` - Transform an error
- `.unwrap()` - Extract value or raise exception
- `.val` - Get value or `None`
- `.err` - Get exception or `None`
- `.is_val` / `.is_err` - Check state

## Pattern Matching

`.match()` provides unified pattern matching for both types and values:

```py
result = (
    fn.expr(42)
    .match()
    .case(int, lambda x: x * 2)
    .case(str, lambda x: len(x))
    .default("unknown")
    .evaluate()
)

assert result.val == 84
```

### Value Matching

```py
result = (
    fn.expr("hello")
    .match()
    .case("hello", "matched!")
    .case("world", "not this")
    .default("nope")
    .evaluate()
)

assert result.val == "matched!"
```

### Direct Values (No Lambdas Needed)

```py
result = (
    fn.expr(5)
    .match()
    .case(int, "is a number")
    .default("not a number")
    .evaluate()
)

assert result.val == "is a number"
```

### Callable Objects with `call=True`

By default, only functions/lambdas are called. Use `call=True` to call other callables:

```py
class MyCallable:
    def __call__(self, x):
        return x * 10

result = (
    fn.expr(5)
    .match()
    .case(int, MyCallable(), call=True)
    .evaluate()
)

assert result.val == 50
```

## Conditional Expressions

`.if_()` uses the truthiness of the wrapped value:

```py
result = fn.expr(True).if_().then(100).else_(200)
assert result.val == 100

result = fn.expr(0).if_().then(100).else_(200)
assert result.val == 200
```

### With Functions

```py
result = fn.expr(True).if_().then(lambda: "yes").else_(lambda: "no")
assert result.val == "yes"
```

### With elif_

```py
result = (
    fn.expr(5)
    .if_()
    .then("small")
    .elif_(lambda: result.val > 10, "medium")
    .else_("tiny")
)
```

## Chaining Example

Everything chains through `Expr`:

```py
result = (
    fn.expr(5)
    .map(lambda x: x * 2)
    .match()
    .case(10, "ten")
    .case(int, lambda x: f"number: {x}")
    .evaluate()
    .if_()
    .then(lambda: "success")
    .else_(lambda: "failed")
)

assert result.val == "success"
```

## Iterator Utilities

`Iterator[T]` provides lazy operations:

```py
result = (
    fn.expr([1, 2, 3, 4])
    .map(lambda xs: fn.iterate(xs))
    .map(lambda it: it.filter(lambda x: x % 2 == 0))
    .map(lambda it: list(it))
)

assert result.val == [2, 4]
```

Common methods: `map`, `filter`, `filterfalse`, `collect`, `chain`, `zip`, `enumerate`, 
`fold`, `reduce`, `flatten`, `sum`, `min`, `max`, and slicing via `[start:stop:step]`.

## Philosophy

**Stay in the monad.** FnUtil encourages you to:

1. Start with `fn.expr(value)`
2. Chain operations (`.map`, `.match`, `.if_`)
3. Only unwrap at the end with `.val` or `.unwrap()`

This ensures consistent error handling and makes your code more composable.
