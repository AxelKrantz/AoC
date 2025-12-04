from textwrap import dedent

from solutions.y2018 import day_21


PROGRAM = dedent(
    """\
    #ip 0
    seti 42 0 1
    eqrr 0 1 2
    addr 2 0 0
    seti 0 0 0
    """
)


def test_part1_detects_first_value() -> None:
    parsed = day_21.parse(PROGRAM)
    assert day_21.solve_part1(parsed) == 42


def test_part2_detects_cycle_last_value() -> None:
    parsed = day_21.parse(PROGRAM)
    assert day_21.solve_part2(parsed) == 42
