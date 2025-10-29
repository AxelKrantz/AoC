from solutions.y2024 import day_01


RAW_EXAMPLE = """\
3 4
4 3
2 5
1 3
3 9
3 3
"""


def test_day01_parts() -> None:
    left, right = day_01.parse(RAW_EXAMPLE)
    assert day_01.solve_part1(left, right) == 11
    assert day_01.solve_part2(left, right) == 31
