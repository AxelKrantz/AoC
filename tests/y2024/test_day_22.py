from solutions.y2024 import day_22


SAMPLE_INPUT = """\
1
10
100
2024
"""


def test_day22_part1_sample() -> None:
    secrets = day_22.parse(SAMPLE_INPUT)
    assert day_22.solve_part1(secrets) == 37327623


def test_day22_part2_sample() -> None:
    secrets = day_22.parse(SAMPLE_INPUT)
    assert day_22.solve_part2(secrets) == 24
