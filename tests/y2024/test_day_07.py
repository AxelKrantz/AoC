from solutions.y2024 import day_07


RAW_EXAMPLE = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def test_day07_parts() -> None:
    equations = day_07.parse(RAW_EXAMPLE)
    assert day_07.solve_part1(equations) == 3749
    assert day_07.solve_part2(equations) == 11387
