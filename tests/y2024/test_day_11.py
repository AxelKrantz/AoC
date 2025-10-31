from solutions.y2024 import day_11


RAW_EXAMPLE = "125 17"


def test_day11_parts() -> None:
    stones = day_11.parse(RAW_EXAMPLE)
    assert day_11.solve_part1(stones) == 55312
    assert day_11.solve_part2(stones) == 65601038650482
