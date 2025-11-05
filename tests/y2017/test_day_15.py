from solutions.y2017 import day_15


SAMPLE = """\
Generator A starts with 65
Generator B starts with 8921
"""


def test_generator_matches_sample() -> None:
    seeds = day_15.parse(SAMPLE)
    assert day_15.count_matches(*seeds, pairs=5) == 1
    assert day_15.count_matches(*seeds, pairs=1056, multiple_a=4, multiple_b=8) == 1
