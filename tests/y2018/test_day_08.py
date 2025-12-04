from solutions.y2018 import day_08


EXAMPLE_INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_part1_example() -> None:
    numbers = day_08.parse(EXAMPLE_INPUT)
    assert day_08.solve_part1(numbers) == 138


def test_part2_example() -> None:
    numbers = day_08.parse(EXAMPLE_INPUT)
    assert day_08.solve_part2(numbers) == 66
