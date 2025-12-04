from textwrap import dedent

from solutions.y2018 import day_13


PART1_EXAMPLE = dedent(
    """\
    /->-\\        
    |   |  /----\\
    | /-+--+-\\  |
    | | |  | v  |
    \\-+-/  \\-+--/
      \\------/   
    """
)

PART2_EXAMPLE = dedent(
    """\
    />-<\\
    |   |
    | /<+-\\
    | | | v
    \\>+</ |
      |   ^
      \\<->/
    """
)


def test_first_collision() -> None:
    track = day_13.parse(PART1_EXAMPLE)
    assert day_13.solve_part1(track) == (7, 3)


def test_last_cart() -> None:
    track = day_13.parse(PART2_EXAMPLE)
    assert day_13.solve_part2(track) == (6, 4)

