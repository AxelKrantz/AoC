from solutions.y2017 import day_13


SAMPLE = """\
0: 3
1: 2
4: 4
6: 4
"""


def test_firewall_severity_example() -> None:
    layers = day_13.parse(SAMPLE)
    assert day_13.solve_part1(layers) == 24
    assert day_13.solve_part2(layers) == 10
