from solutions.y2017 import day_09


def test_stream_score_examples() -> None:
    assert day_09.solve_part1("{}") == 1
    assert day_09.solve_part1("{{{}}}") == 6
    assert day_09.solve_part1("{{},{}}") == 5
    assert day_09.solve_part1("{{{},{},{{}}}}") == 16
    assert day_09.solve_part1("{<a>,<a>,<a>,<a>}") == 1
    assert day_09.solve_part1("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
    assert day_09.solve_part1("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
    assert day_09.solve_part1("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3


def test_garbage_count_examples() -> None:
    assert day_09.solve_part2("<>") == 0
    assert day_09.solve_part2("<random characters>") == 17
    assert day_09.solve_part2("<<<<>") == 3
    assert day_09.solve_part2("<{!>}>") == 2
    assert day_09.solve_part2("<!!>") == 0
    assert day_09.solve_part2("<!!!>>") == 0
    assert day_09.solve_part2("<{o\"i!a,<{i<a>") == 10
