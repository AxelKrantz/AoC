from solutions.y2024 import day_14


RAW_EXAMPLE = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def test_day14_parts() -> None:
    robots = day_14.parse(RAW_EXAMPLE)
    assert day_14.solve_part1(robots, width=11, height=7) == 12
    seconds, state = day_14.solve_part2(robots, width=11, height=7)
    assert day_14.max_horizontal_run(state) == 4
