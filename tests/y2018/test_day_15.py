from solutions.y2018 import day_15


EXAMPLE_PART1 = "\n".join(
    [
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ]
)

EXAMPLE_PART1_ALT = "\n".join(
    [
        "#######",
        "#G..#E#",
        "#E#E.E#",
        "#G.##.#",
        "#...#E#",
        "#...E.#",
        "#######",
    ]
)

EXAMPLE_PART2 = "\n".join(
    [
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ]
)


def test_part1_examples() -> None:
    assert day_15.solve_part1(day_15.parse(EXAMPLE_PART1)) == 27730
    assert day_15.solve_part1(day_15.parse(EXAMPLE_PART1_ALT)) == 36334


def test_part2_example() -> None:
    assert day_15.solve_part2(day_15.parse(EXAMPLE_PART1)) == 4988
    assert day_15.solve_part2(day_15.parse(EXAMPLE_PART2)) == 31284
