from solutions.y2024 import day_02


RAW_EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_day02_parts() -> None:
    reports = day_02.parse(RAW_EXAMPLE)
    assert day_02.solve_part1(reports) == 2
    assert day_02.solve_part2(reports) == 4
