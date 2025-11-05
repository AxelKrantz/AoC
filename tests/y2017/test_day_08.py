from solutions.y2017 import day_08


SAMPLE = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""


def test_register_instructions_example() -> None:
    instructions = day_08.parse(SAMPLE)
    assert day_08.solve_part1(instructions) == 1
    assert day_08.solve_part2(instructions) == 10
