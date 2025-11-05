from solutions.y2016 import day_02


EXAMPLE = """\
ULL
RRDDD
LURDL
UUUUD
"""


def test_square_keypad_code() -> None:
    instructions = day_02.parse(EXAMPLE)
    assert day_02.solve_part1(instructions) == "1985"


def test_diamond_keypad_code() -> None:
    instructions = day_02.parse(EXAMPLE)
    assert day_02.solve_part2(instructions) == "5DB3"
