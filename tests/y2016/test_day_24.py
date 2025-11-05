from solutions.y2016 import day_24


SAMPLE = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""


def test_shortest_route_example() -> None:
    parsed = day_24.parse(SAMPLE)
    assert day_24.solve_part1(parsed) == 14
    assert day_24.solve_part2(parsed) == 20
