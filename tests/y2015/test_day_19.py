from solutions.y2015 import day_19


SAMPLE = """\
e => H
e => O
H => HO
H => OH
O => HH

HOH
"""

SAMPLE_LARGE = """\
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
"""


def test_distinct_molecules_example() -> None:
    data = day_19.parse(SAMPLE)
    assert day_19.solve_part1(data) == 4
    assert day_19.solve_part2(data) == 3


def test_formula_handles_larger_example() -> None:
    data = day_19.parse(SAMPLE_LARGE)
    assert day_19.solve_part2(data) == 6
