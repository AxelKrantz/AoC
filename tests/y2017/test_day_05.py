from solutions.y2017 import day_05


SAMPLE = """\
0
3
0
1
-3
"""


def test_trampoline_steps() -> None:
    offsets = day_05.parse(SAMPLE)
    assert day_05.solve_part1(offsets) == 5
    assert day_05.solve_part2(offsets) == 10
