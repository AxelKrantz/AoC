from solutions.y2024 import day_09


RAW_EXAMPLE = "2333133121414131402"


def test_day09_parts() -> None:
    disk_map = day_09.parse(RAW_EXAMPLE)
    assert day_09.solve_part1(disk_map) == 1928
    assert day_09.solve_part2(disk_map) == 2858
