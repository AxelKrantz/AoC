from solutions.y2015 import day_24


SAMPLE = """\
1
2
3
4
5
7
8
9
10
11
"""


def test_quantum_entanglement_minimization() -> None:
    weights = day_24.parse(SAMPLE)
    assert day_24.solve_part1(weights) == 99
    assert day_24.solve_part2(weights) == 44
