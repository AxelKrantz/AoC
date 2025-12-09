from solutions.y2025 import day_09


EXAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def test_part1_example() -> None:
    points = day_09.parse(EXAMPLE)
    assert day_09.solve_part1(points) == 50


def test_part2_example() -> None:
    points = day_09.parse(EXAMPLE)
    assert day_09.solve_part2(points) == 24
