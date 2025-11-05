from solutions.y2017 import day_01


def test_part1_examples() -> None:
    assert day_01.solve_part1("1122") == 3
    assert day_01.solve_part1("1111") == 4
    assert day_01.solve_part1("1234") == 0
    assert day_01.solve_part1("91212129") == 9


def test_part2_examples() -> None:
    assert day_01.solve_part2("1212") == 6
    assert day_01.solve_part2("1221") == 0
    assert day_01.solve_part2("123425") == 4
    assert day_01.solve_part2("123123") == 12
    assert day_01.solve_part2("12131415") == 4
