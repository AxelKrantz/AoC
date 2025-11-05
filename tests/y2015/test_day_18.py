from solutions.y2015 import day_18


SAMPLE = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""


def test_animated_lights_examples() -> None:
    data = day_18.parse(SAMPLE)
    assert day_18.solve_part1(data, steps=4) == 4
    assert day_18.solve_part2(data, steps=5) == 17
