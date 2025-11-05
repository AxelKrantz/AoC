from solutions.y2017 import day_12


SAMPLE = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""


def test_program_groups_example() -> None:
    graph = day_12.parse(SAMPLE)
    assert day_12.solve_part1(graph) == 6
    assert day_12.solve_part2(graph) == 2
