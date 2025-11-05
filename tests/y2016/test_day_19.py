from solutions.y2016 import day_19


def test_josephus_examples() -> None:
    assert day_19.solve_part1(5) == 3
    assert day_19.solve_part2(5) == 2
