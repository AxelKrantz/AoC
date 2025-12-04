from solutions.y2025 import day_01


RAW_EXAMPLE = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def test_part1_example() -> None:
    rotations = day_01.parse(RAW_EXAMPLE)
    assert day_01.solve_part1(rotations) == 3


def test_part2_example() -> None:
    rotations = day_01.parse(RAW_EXAMPLE)
    assert day_01.solve_part2(rotations) == 6
