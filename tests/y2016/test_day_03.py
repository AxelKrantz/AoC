from solutions.y2016 import day_03


EXAMPLE = """\
  5 10 25
  3  4  5
  2  3  4
  6  8 10
  7  9 12
  9 12 15
"""


def test_invalid_triangle_detection() -> None:
    triangles = day_03.parse(EXAMPLE)
    assert day_03.solve_part1(triangles) == 5


def test_vertical_grouping() -> None:
    triangles = day_03.parse(EXAMPLE)
    assert day_03.solve_part2(triangles) == 3
