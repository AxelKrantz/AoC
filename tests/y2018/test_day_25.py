from textwrap import dedent

from solutions.y2018 import day_25


SAMPLE_A = dedent(
    """\
    0,0,0,0
    3,0,0,0
    0,3,0,0
    0,0,3,0
    0,0,0,3
    0,0,0,6
    9,0,0,0
    12,0,0,0
    """
)

SAMPLE_B = dedent(
    """\
    -1,2,2,0
    0,0,2,-2
    0,0,0,-2
    -1,2,0,0
    -2,-2,-2,2
    3,0,2,-1
    -1,3,2,2
    -1,0,-1,0
    0,2,1,-2
    3,0,0,0
    """
)


def test_part1_examples() -> None:
    assert day_25.solve_part1(day_25.parse(SAMPLE_A)) == 2
    assert day_25.solve_part1(day_25.parse(SAMPLE_B)) == 4


def test_part2_returns_zero() -> None:
    assert day_25.solve_part2(day_25.parse(SAMPLE_A)) == 0
