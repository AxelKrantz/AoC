from solutions.y2024 import day_03


def test_day03_part1_sample() -> None:
    program = "mul(2,4)mul(3,5)mul(10,10)"
    assert day_03.solve_part1(program) == (2 * 4 + 3 * 5 + 10 * 10)


def test_day03_part2_with_switches() -> None:
    program = "mul(1,2)don't()mul(2,3)do()mul(3,4)"
    assert day_03.solve_part2(program) == (1 * 2 + 3 * 4)
