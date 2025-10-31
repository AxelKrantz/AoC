from solutions.y2024 import day_12


SAMPLE_1 = """\
AAAA
BBCD
BBCC
EEEC
"""

SAMPLE_2 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

SAMPLE_3 = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


def test_day12_example_one() -> None:
    grid = day_12.parse(SAMPLE_1)
    assert day_12.solve_part1(grid) == 140
    assert day_12.solve_part2(grid) == 80


def test_day12_example_two() -> None:
    grid = day_12.parse(SAMPLE_2)
    assert day_12.solve_part1(grid) == 772
    assert day_12.solve_part2(grid) == 436


def test_day12_example_three() -> None:
    grid = day_12.parse(SAMPLE_3)
    assert day_12.solve_part1(grid) == 1930
    assert day_12.solve_part2(grid) == 1206
