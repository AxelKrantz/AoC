from solutions.y2017 import day_17


def test_spinlock_example() -> None:
    assert day_17.solve_part1(3) == 638
    assert day_17.solve_part2(3, insertions=9) == 9
