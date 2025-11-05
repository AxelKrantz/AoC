from solutions.y2016 import day_13


def test_shortest_path_example() -> None:
    puzzle_input = day_13.parse("10")
    assert day_13.solve_part1(puzzle_input, target=(7, 4)) == 11
