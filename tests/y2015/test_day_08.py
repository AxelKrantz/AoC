from solutions.y2015 import day_08


EXAMPLE = ['""', '"abc"', '"aaa\\"aaa"', '"\\x27"']


def test_part1_example() -> None:
    assert day_08.solve_part1(EXAMPLE) == 12


def test_part2_example() -> None:
    assert day_08.solve_part2(EXAMPLE) == 19
