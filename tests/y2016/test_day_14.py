from solutions.y2016 import day_14


def test_example_key_indices() -> None:
    salt = day_14.parse("abc")
    assert day_14.solve_part1(salt) == 22728
    assert day_14.solve_part2(salt) == 22551
