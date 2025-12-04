from solutions.y2018 import day_11


def test_part1_examples() -> None:
    assert day_11.solve_part1(18) == (33, 45)
    assert day_11.solve_part1(42) == (21, 61)


def test_part2_examples() -> None:
    assert day_11.solve_part2(18) == (90, 269, 16)
    assert day_11.solve_part2(42) == (232, 251, 12)

