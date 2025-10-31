from solutions.y2024 import day_17


SAMPLE_INPUT = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


def test_day17_part1_sample() -> None:
    initial, program = day_17.parse(SAMPLE_INPUT)
    assert day_17.solve_part1(initial, program) == "4,6,3,5,6,3,5,2,1,0"


def test_day17_part2_sample_matches_program() -> None:
    initial, program = day_17.parse(SAMPLE_INPUT)
    try:
        day_17.solve_part2(initial, program)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected no solution for sample part 2 input.")


REAL_INPUT = """\
Register A: 28422061
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,1,5,4,2,5,5,0,3,3,0
"""


def test_day17_part2_actual_input_behaviour() -> None:
    initial, program = day_17.parse(REAL_INPUT)
    result = day_17.solve_part2(initial, program)
    outputs = day_17.run_program(
        day_17.MachineState(result, initial.b, initial.c), program
    )
    assert outputs == list(program)
