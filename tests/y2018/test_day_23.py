from textwrap import dedent

from solutions.y2018 import day_23


PART1_SAMPLE = dedent(
    """\
    pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1
    """
)


PART2_SAMPLE = dedent(
    """\
    pos=<10,12,12>, r=2
    pos=<12,14,12>, r=2
    pos=<16,12,12>, r=4
    pos=<14,14,14>, r=6
    pos=<50,50,50>, r=200
    pos=<10,10,10>, r=5
    """
)


def test_part1_example() -> None:
    bots = day_23.parse(PART1_SAMPLE)
    assert day_23.solve_part1(bots) == 7


def test_part2_example() -> None:
    bots = day_23.parse(PART2_SAMPLE)
    assert day_23.solve_part2(bots) == 36
