from solutions.y2017 import day_21


SAMPLE = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""


def test_fractal_art_example() -> None:
    rules = day_21.parse(SAMPLE)
    assert day_21.solve_part1(rules, iterations=2) == 12
