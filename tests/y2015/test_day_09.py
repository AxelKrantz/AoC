from solutions.y2015 import day_09


EXAMPLE = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""


def test_routes() -> None:
    routes = day_09.parse(EXAMPLE)
    assert day_09.solve_part1(routes) == 605
    assert day_09.solve_part2(routes) == 982
