from solutions.y2017 import day_02


PART1_SAMPLE = """\
5 1 9 5
7 5 3
2 4 6 8
"""


PART2_SAMPLE = """\
5 9 2 8
9 4 7 3
3 8 6 5
"""


def test_checksum_part1() -> None:
    rows = day_02.parse(PART1_SAMPLE)
    assert day_02.solve_part1(rows) == 18


def test_checksum_part2() -> None:
    rows = day_02.parse(PART2_SAMPLE)
    assert day_02.solve_part2(rows) == 9
