from solutions.y2016 import day_25


SIMPLE = """\
out 0
out 1
jnz 1 -2
"""


def test_clock_signal_detection() -> None:
    program = day_25.parse(SIMPLE)
    assert day_25.is_clock_signal(program, 0, required=6) is True
    assert day_25.solve_part1(program) == 0
