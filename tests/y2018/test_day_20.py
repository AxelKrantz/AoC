from solutions.y2018 import day_20


def test_part1_simple_examples() -> None:
    assert day_20.solve_part1("^WNE$") == 3
    assert day_20.solve_part1("^ENWWW(NEEE|SSE(EE|N))$") == 10


def test_part2_threshold_count() -> None:
    assert day_20.solve_part2("^WNE$", threshold=2) == 2
