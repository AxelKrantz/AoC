from solutions.y2015 import day_07


EXAMPLE = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""


def test_example_signals() -> None:
    expressions = day_07.parse(EXAMPLE)
    evaluator = day_07.Evaluator(expressions)
    assert evaluator.evaluate("d") == 72
    assert evaluator.evaluate("e") == 507
    assert evaluator.evaluate("f") == 492
    assert evaluator.evaluate("g") == 114
    assert evaluator.evaluate("h") == 65412
    assert evaluator.evaluate("i") == 65079
    assert evaluator.evaluate("x") == 123
    assert evaluator.evaluate("y") == 456


def test_part2_override() -> None:
    expressions = day_07.parse(
        "\n".join(
            [
                "123 -> x",
                "456 -> b",
                "x AND b -> a",
            ]
        )
    )
    part1 = day_07.solve_part1(expressions)
    assert part1 == 72
    assert day_07.solve_part2(expressions) == 72
