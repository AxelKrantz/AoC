from solutions.y2017 import day_18


PART1_SAMPLE = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
set a 1
rcv a
"""


PART2_SAMPLE = """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
"""


def test_duet_recover_example() -> None:
    instructions = day_18.parse(PART1_SAMPLE)
    assert day_18.solve_part1(instructions) == 4


def test_duet_parallel_example() -> None:
    instructions = day_18.parse(PART2_SAMPLE)
    assert day_18.solve_part2(instructions) == 3
