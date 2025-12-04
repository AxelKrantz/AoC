from solutions.y2018 import day_06


EXAMPLE_INPUT = "\n".join(
    [
        "1, 1",
        "1, 6",
        "8, 3",
        "3, 4",
        "5, 5",
        "8, 9",
    ]
)


def test_part1_example() -> None:
    points = day_06.parse(EXAMPLE_INPUT)
    assert day_06.solve_part1(points) == 17


def test_part2_example() -> None:
    points = day_06.parse(EXAMPLE_INPUT)
    assert day_06.solve_part2(points, limit=32) == 16

