from solutions.y2016 import day_20


SAMPLE = """\
5-8
0-2
4-7
"""


def test_blocked_ip_example() -> None:
    ranges = day_20.parse(SAMPLE)
    assert day_20.solve_part1(ranges, max_value=9) == 3
    assert day_20.solve_part2(ranges, max_value=9) == 2
