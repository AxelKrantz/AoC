from solutions.y2016 import day_23


SAMPLE = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""


def test_toggling_program_example() -> None:
    program = day_23.parse(SAMPLE)
    registers = day_23.run(program, {"a": 0})
    assert registers["a"] == 3
