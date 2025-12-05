from solutions.y2025 import day_05


RAW_EXAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def test_part1_example() -> None:
    parsed = day_05.parse(RAW_EXAMPLE)
    assert day_05.solve_part1(parsed) == 3


def test_part2_example() -> None:
    ranges, _ = day_05.parse(RAW_EXAMPLE)
    assert day_05.solve_part2(ranges) == 14
