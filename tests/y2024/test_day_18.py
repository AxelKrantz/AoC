from solutions.y2024 import day_18


SAMPLE_INPUT = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def test_day18_part1_sample() -> None:
    coordinates = day_18.parse(SAMPLE_INPUT)
    assert day_18.solve_part1(coordinates, grid_size=6, byte_limit=12) == 22


def test_day18_part2_sample() -> None:
    coordinates = day_18.parse(SAMPLE_INPUT)
    assert day_18.solve_part2(coordinates, grid_size=6) == "6,1"
