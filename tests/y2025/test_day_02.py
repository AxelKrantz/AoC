from solutions.y2025 import day_02


RAW_EXAMPLE = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


def test_part1_example() -> None:
    ranges = day_02.parse(RAW_EXAMPLE)
    assert day_02.solve_part1(ranges) == 1227775554


def test_part2_example() -> None:
    ranges = day_02.parse(RAW_EXAMPLE)
    assert day_02.solve_part2(ranges) == 4174379265
