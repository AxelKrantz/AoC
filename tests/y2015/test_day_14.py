from solutions.y2015 import day_14


SAMPLE = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""


def test_sample_distances() -> None:
    herd = day_14.parse(SAMPLE)
    assert day_14.solve_part1(herd, duration=1000) == 1120
    assert day_14.solve_part2(herd, duration=1000) == 689
