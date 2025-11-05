from solutions.y2015 import day_16


SAMPLE = """\
Sue 1: trees: 4, goldfish: 4, cars: 2
Sue 2: cars: 2, vizslas: 0
Sue 3: perfumes: 1, children: 3
"""


def test_identify_correct_sue() -> None:
    sues = day_16.parse(SAMPLE)
    assert day_16.solve_part1(sues) == 2
    assert day_16.solve_part2(sues) == 1
