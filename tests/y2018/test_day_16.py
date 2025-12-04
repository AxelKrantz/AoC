from solutions.y2018 import day_16


EXAMPLE_PART1 = (
    "Before: [3, 2, 1, 1]\n"
    "9 2 1 2\n"
    "After:  [3, 2, 2, 1]\n"
    "\n"
    "\n"
    "\n"
    "\n"
    "9 2 1 2\n"
)

CUSTOM_INPUT = (
    "Before: [2, 0, 0, 0]\n"
    "0 0 3 0\n"
    "After:  [5, 0, 0, 0]\n"
    "\n"
    "Before: [2, 3, 0, 0]\n"
    "1 0 1 2\n"
    "After:  [2, 3, 6, 0]\n"
    "\n"
    "Before: [0, 0, 0, 0]\n"
    "2 2 0 1\n"
    "After:  [0, 2, 0, 0]\n"
    "\n"
    "\n"
    "\n"
    "\n"
    "0 0 3 0\n"
    "2 3 0 1\n"
    "1 0 1 0\n"
)


def test_part1_example() -> None:
    puzzle = day_16.parse(EXAMPLE_PART1)
    assert day_16.solve_part1(puzzle) == 1


def test_part2_custom_program() -> None:
    puzzle = day_16.parse(CUSTOM_INPUT)
    assert day_16.solve_part2(puzzle) == 9
