from solutions.y2016 import day_16


def test_dragon_curve_example() -> None:
    state = day_16.parse("10000")
    assert day_16.solve(state, 20) == "01100"
