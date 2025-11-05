from solutions.y2017 import day_06


def test_memory_reallocation_example() -> None:
    banks = day_06.parse("0 2 7 0")
    assert day_06.solve_part1(banks) == 5
    assert day_06.solve_part2(banks) == 4
