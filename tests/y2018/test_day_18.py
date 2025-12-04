from textwrap import dedent

from solutions.y2018 import day_18


SAMPLE_INPUT = dedent(
    """\
    .#.#...|#.
    .....#|##|
    .|..|...#.
    ..|#.....#
    #.#|||#|#|
    ...#.||...
    .|....|...
    ||...#|.#|
    |.||||..#|
    ...#.|..|.
    """
)


def test_part1_example() -> None:
    area = day_18.parse(SAMPLE_INPUT)
    assert day_18.solve_part1(area) == 1120


def test_part2_example_cycle_detection() -> None:
    area = day_18.parse(SAMPLE_INPUT)
    assert day_18.solve_part2(area) == 0
