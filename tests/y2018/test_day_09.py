from solutions.y2018 import day_09


def test_part1_small_example() -> None:
    game = day_09.parse("9 players; last marble is worth 25 points")
    assert day_09.solve_part1(game) == 32


def test_part1_larger_examples() -> None:
    assert (
        day_09.solve_part1(day_09.parse("10 players; last marble is worth 1618 points"))
        == 8317
    )
    assert (
        day_09.solve_part1(day_09.parse("13 players; last marble is worth 7999 points"))
        == 146373
    )


def test_part2_example() -> None:
    game = day_09.parse("10 players; last marble is worth 1618 points")
    assert day_09.solve_part2(game) == 74765078

