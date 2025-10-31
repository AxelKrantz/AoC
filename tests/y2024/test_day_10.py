from solutions.y2024 import day_10


RAW_EXAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def test_day10_parts() -> None:
    grid = day_10.parse(RAW_EXAMPLE)
    assert day_10.solve_part1(grid) == 36
    assert day_10.solve_part2(grid) == 81
