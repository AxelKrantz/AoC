from solutions.y2016 import day_21


SAMPLE = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""


def test_scramble_example() -> None:
    operations = day_21.parse(SAMPLE)
    assert day_21.solve_part1(operations, starting="abcde") == "decab"
    assert day_21.solve_part2(operations, scrambled="decab") == "abcde"
