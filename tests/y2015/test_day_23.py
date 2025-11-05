from solutions.y2015 import day_23


def test_sample_program_advances_register_a() -> None:
    program = day_23.parse(
        """inc a
jio a, +2
tpl a
inc a
"""
    )
    registers = day_23.run(program, register_a=0, register_b=0)
    assert registers["a"] == 2


def test_branching_program_updates_register_b() -> None:
    program = day_23.parse(
        """jio a, +2
inc b
jmp +2
inc b
inc b
"""
    )
    assert day_23.solve_part1(program) == 2
    assert day_23.solve_part2(program) == 1
