from solutions.y2017 import day_22


SAMPLE = """\
..#
#..
...
"""


def test_sporifica_virus_example() -> None:
    grid = day_22.parse(SAMPLE)
    assert day_22.solve_part1(grid, bursts=7) == 5
    assert day_22.solve_part2(grid, bursts=100) == 26
