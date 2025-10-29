from solutions.y2024 import day_04


RAW_EXAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def test_day04_parts() -> None:
    grid = day_04.parse(RAW_EXAMPLE)
    assert day_04.solve_part1(grid) == 18
    assert day_04.solve_part2(grid) == 9
