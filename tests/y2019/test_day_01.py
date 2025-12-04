from solutions.y2019 import day_01


def test_part1_examples() -> None:
    assert day_01.solve_part1([12]) == 2
    assert day_01.solve_part1([14]) == 2
    assert day_01.solve_part1([1969]) == 654
    assert day_01.solve_part1([100756]) == 33583


def test_part2_examples() -> None:
    assert day_01.solve_part2([14]) == 2
    assert day_01.solve_part2([1969]) == 966
    assert day_01.solve_part2([100756]) == 50346
