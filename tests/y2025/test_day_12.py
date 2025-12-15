from solutions.y2025 import day_12


EXAMPLE = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def test_part1_example() -> None:
    parsed = day_12.parse(EXAMPLE)
    assert day_12.solve_part1(parsed) == 2


def test_part2_trivial() -> None:
    parsed = day_12.parse(EXAMPLE)
    assert day_12.solve_part2(parsed) == 0
