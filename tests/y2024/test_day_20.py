from solutions.y2024 import day_20


SAMPLE_INPUT = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def test_day20_sample_counts_limit2() -> None:
    grid = day_20.parse(SAMPLE_INPUT)
    assert day_20.count_cheats(grid, cheat_limit=2, min_savings=20) == 5
    assert day_20.count_cheats(grid, cheat_limit=2, min_savings=50) == 1


def test_day20_sample_limit20_threshold50() -> None:
    grid = day_20.parse(SAMPLE_INPUT)
    assert day_20.count_cheats(grid, cheat_limit=20, min_savings=50) == 285
