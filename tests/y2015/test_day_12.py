from solutions.y2015 import day_12


def test_sum_numbers_examples() -> None:
    assert day_12.solve_part1([1, 2, 3]) == 6
    assert day_12.solve_part1({"a": 2, "b": 4}) == 6
    assert day_12.solve_part1({"a": {"b": 4}, "c": -1}) == 3


def test_skip_red_examples() -> None:
    assert day_12.solve_part2([1, {"c": "red", "b": 2}, 3]) == 4
    assert day_12.solve_part2({"d": "red", "e": [1, 2, 3, 4], "f": 5}) == 0
