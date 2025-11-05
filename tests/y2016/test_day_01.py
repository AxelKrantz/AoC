from solutions.y2016 import day_01


def test_part1_examples() -> None:
    instructions = day_01.parse("R2, L3")
    assert day_01.solve_part1(instructions) == 5
    instructions = day_01.parse("R2, R2, R2")
    assert day_01.solve_part1(instructions) == 2
    instructions = day_01.parse("R5, L5, R5, R3")
    assert day_01.solve_part1(instructions) == 12


def test_part2_example() -> None:
    instructions = day_01.parse("R8, R4, R4, R8")
    assert day_01.solve_part2(instructions) == 4
