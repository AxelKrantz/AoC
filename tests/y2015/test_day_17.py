from solutions.y2015 import day_17


def test_container_combinations_example() -> None:
    containers = [20, 15, 10, 5, 5]
    assert day_17.solve_part1(containers, target=25) == 4
    assert day_17.solve_part2(containers, target=25) == 3
