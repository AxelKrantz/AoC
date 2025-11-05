from solutions.y2017 import day_03


def test_manhattan_distances() -> None:
    assert day_03.solve_part1(1) == 0
    assert day_03.solve_part1(12) == 3
    assert day_03.solve_part1(23) == 2
    assert day_03.solve_part1(1024) == 31


def test_spiral_sum_sequence() -> None:
    assert day_03.solve_part2(1) == 2
    assert day_03.solve_part2(2) == 4
    assert day_03.solve_part2(4) == 5
    assert day_03.solve_part2(747) == 806
