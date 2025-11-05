from solutions.y2016 import day_11


SAMPLE = """\
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""


def test_minimum_steps_example() -> None:
    facility = day_11.parse(SAMPLE)
    assert day_11.solve_part1(facility) == 11
