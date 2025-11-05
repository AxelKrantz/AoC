from solutions.y2016 import day_12


SAMPLE = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""


def test_assembunny_interpreter() -> None:
    instructions = day_12.parse(SAMPLE)
    assert day_12.solve_part1(instructions) == 42
