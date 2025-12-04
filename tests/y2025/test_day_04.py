from solutions.y2025 import day_04


RAW_EXAMPLE = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def test_part1_example() -> None:
    grid = day_04.parse(RAW_EXAMPLE)
    assert day_04.solve_part1(grid) == 13


def test_part2_example() -> None:
    grid = day_04.parse(RAW_EXAMPLE)
    assert day_04.solve_part2(grid) == 43
