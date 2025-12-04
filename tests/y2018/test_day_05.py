from solutions.y2018 import day_05


EXAMPLE = "dabAcCaCBAcCcaDA"


def test_part1_example() -> None:
    polymer = day_05.parse(EXAMPLE)
    assert day_05.solve_part1(polymer) == 10


def test_part2_example() -> None:
    polymer = day_05.parse(EXAMPLE)
    assert day_05.solve_part2(polymer) == 4

