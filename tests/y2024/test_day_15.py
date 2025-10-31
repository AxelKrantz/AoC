from solutions.y2024 import day_15


RAW_SMALL = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""


def test_day15_small_example() -> None:
    grid, moves = day_15.parse(RAW_SMALL)
    result = day_15.solve_part1([row[:] for row in grid], moves)
    assert result == 2028
    result_part2 = day_15.solve_part2([row[:] for row in grid], moves)
    assert result_part2 == 1751
