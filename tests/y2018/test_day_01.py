from solutions.y2018 import day_01


def test_part1_examples() -> None:
    assert day_01.solve_part1(day_01.parse("+1\n-2\n+3\n+1")) == 3
    assert day_01.solve_part1(day_01.parse("+1\n+1\n+1")) == 3
    assert day_01.solve_part1(day_01.parse("+1\n+1\n-2")) == 0
    assert day_01.solve_part1(day_01.parse("-1\n-2\n-3")) == -6


def test_part2_examples() -> None:
    assert day_01.solve_part2(day_01.parse("+1\n-2\n+3\n+1")) == 2
    assert day_01.solve_part2(day_01.parse("+1\n-1")) == 0
    assert day_01.solve_part2(day_01.parse("+3\n+3\n+4\n-2\n-4")) == 10
    assert day_01.solve_part2(day_01.parse("-6\n+3\n+8\n+5\n-6")) == 5
    assert day_01.solve_part2(day_01.parse("+7\n+7\n-2\n-7\n-4")) == 14

