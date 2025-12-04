from textwrap import dedent

from solutions.y2018 import day_22


SAMPLE_INPUT = dedent(
    """\
    depth: 510
    target: 10,10
    """
)


def test_part1_example() -> None:
    parsed = day_22.parse(SAMPLE_INPUT)
    assert day_22.solve_part1(parsed) == 114


def test_part2_example() -> None:
    parsed = day_22.parse(SAMPLE_INPUT)
    assert day_22.solve_part2(parsed, margin=20) == 45
