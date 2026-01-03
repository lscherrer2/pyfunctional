from fnutil import expr

res = (
    expr(False).match_type().case(int, lambda x: int).default(lambda x: None).evaluate()
)
res = (
    expr(8)
    .match_type()
    .case(bool, lambda x: "bool")
    .case(int | float, lambda x: "number")
    .default(lambda x: "default")
    .evaluate()
)


res = (
    expr(False)
    .match_value()
    .case(True, lambda x: "true")
    .case(False, lambda x: "false")
    .default(lambda x: "default")
)

res = (
    expr(8)
    .match_value()
    .case(True, lambda x: "true")
    .case(False, lambda x: "false")
    .default(lambda x: "default")
)

res = (
    expr(8)
    .match_value()
    .case(True, lambda x: "true")
    .case(8, lambda x: "number")
    .default(lambda x: "default")
)
