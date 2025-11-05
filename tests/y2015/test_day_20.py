from solutions.y2015 import day_20


def test_presents_thresholds_small_targets() -> None:
    assert day_20.solve_part1(70) == 4
    assert day_20.solve_part1(150) == 8
    assert day_20.solve_part2(66) == 4
    assert day_20.solve_part2(100) == 6
