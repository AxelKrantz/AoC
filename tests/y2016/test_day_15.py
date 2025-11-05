from solutions.y2016 import day_15


SAMPLE = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""


def test_disc_alignment_example() -> None:
    discs = day_15.parse(SAMPLE)
    assert day_15.solve_part1(discs) == 5
