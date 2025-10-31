from solutions.y2024 import day_21


SAMPLE_INPUT = """\
029A
980A
179A
456A
379A
"""


def test_day21_part1_sample() -> None:
    codes = day_21.parse(SAMPLE_INPUT)
    assert day_21.solve_part1(codes) == 126384


def test_day21_part2_sample() -> None:
    codes = day_21.parse(SAMPLE_INPUT)
    assert day_21.solve_part2(codes) == 154115708116294
