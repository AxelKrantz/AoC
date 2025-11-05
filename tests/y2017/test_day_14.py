from solutions.y2017 import day_14


def test_disk_defragmentation_example() -> None:
    key = day_14.parse("flqrgnkx")
    assert day_14.solve_part1(key) == 8108
    assert day_14.solve_part2(key) == 1242
