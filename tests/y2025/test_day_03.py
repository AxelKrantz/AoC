from solutions.y2025 import day_03


RAW_EXAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""


def test_part1_example() -> None:
    banks = day_03.parse(RAW_EXAMPLE)
    assert day_03.solve_part1(banks) == 357


def test_part2_example() -> None:
    banks = day_03.parse(RAW_EXAMPLE)
    assert day_03.solve_part2(banks) == 3121910778619
