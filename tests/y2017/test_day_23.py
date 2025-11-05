from solutions.y2017 import day_23


PART1_SAMPLE = """\
set a 2
mul a a
sub a 1
mul a 2
jnz a 2
mul a 2
"""


PART2_SAMPLE = """\
set b 10
set c b
jnz a 2
jnz 1 5
mul b 1
sub b -0
set c b
sub c -10
"""


def test_coprocessor_mul_count() -> None:
    instructions = day_23.parse(PART1_SAMPLE)
    assert day_23.solve_part1(instructions) == 2


def test_coprocessor_composite_count() -> None:
    instructions = day_23.parse(PART2_SAMPLE)
    assert day_23.solve_part2(instructions) == 1
