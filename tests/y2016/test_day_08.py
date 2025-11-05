from solutions.y2016 import day_08


SAMPLE = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""


EXPECTED = """\
.#..#.#
#.#....
.#.....
"""


def test_screen_operations() -> None:
    instructions = day_08.parse(SAMPLE)
    pixels = day_08.apply(instructions, width=7, height=3)
    assert len(pixels) == 6
    assert day_08.render(pixels, width=7, height=3) == EXPECTED.strip()
