from solutions.y2015 import day_15


SAMPLE = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""


def test_cookie_scoring_examples() -> None:
    ingredients = day_15.parse(SAMPLE)
    assert day_15.solve_part1(ingredients) == 62842880
    assert day_15.solve_part2(ingredients) == 57600000
