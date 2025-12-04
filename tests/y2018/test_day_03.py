from solutions.y2018 import day_03


EXAMPLE_INPUT = "\n".join(
    [
        "#1 @ 1,3: 4x4",
        "#2 @ 3,1: 4x4",
        "#3 @ 5,5: 2x2",
    ]
)


def test_part1_example() -> None:
    claims = day_03.parse(EXAMPLE_INPUT)
    assert day_03.solve_part1(claims) == 4


def test_part2_example() -> None:
    claims = day_03.parse(EXAMPLE_INPUT)
    assert day_03.solve_part2(claims) == 3

