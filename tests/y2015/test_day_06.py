from solutions.y2015 import day_06


def test_part1_examples() -> None:
    instructions = day_06.parse(
        "\n".join(
            [
                "turn on 0,0 through 999,999",
            ]
        )
    )
    assert day_06.solve_part1(instructions) == 1_000_000


def test_part2_examples() -> None:
    instructions = day_06.parse(
        "\n".join(
            [
                "turn on 0,0 through 0,0",
                "toggle 0,0 through 999,999",
            ]
        )
    )
    assert day_06.solve_part2(instructions) == 2_000_001
