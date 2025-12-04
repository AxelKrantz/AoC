from textwrap import dedent

from solutions.y2018 import day_19


def test_part1_example() -> None:
    raw = dedent(
        """\
        #ip 0
        seti 5 0 1
        seti 6 0 2
        addi 0 1 0
        addr 1 2 3
        setr 1 0 0
        seti 8 0 4
        seti 9 0 5
        """
    )
    program = day_19.parse(raw)
    assert day_19.solve_part1(program) == 6


def test_sum_of_divisors_helper() -> None:
    assert day_19.sum_of_divisors(28) == 56
