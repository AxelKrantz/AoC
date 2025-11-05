from solutions.y2017 import day_24


SAMPLE = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
"""


def test_electromagnetic_moat_example() -> None:
    components = day_24.parse(SAMPLE)
    assert day_24.solve_part1(components) == 31
    assert day_24.solve_part2(components) == 19
