from solutions.y2018 import day_17


SAMPLE_INPUT = "\n".join(
    [
        "x=495, y=2..7",
        "y=7, x=495..501",
        "x=501, y=3..7",
        "x=498, y=2..4",
        "x=506, y=1..2",
        "x=498, y=10..13",
        "x=504, y=10..13",
        "y=13, x=498..504",
    ]
)


def test_part1_example() -> None:
    reservoir = day_17.parse(SAMPLE_INPUT)
    assert day_17.solve_part1(reservoir) == 57


def test_part2_example() -> None:
    reservoir = day_17.parse(SAMPLE_INPUT)
    assert day_17.solve_part2(reservoir) == 29
