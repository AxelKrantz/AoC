from solutions.y2024 import day_19


SAMPLE_INPUT = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def test_day19_part1_sample() -> None:
    patterns, designs = day_19.parse(SAMPLE_INPUT)
    assert day_19.solve_part1(patterns, designs) == 6


def test_day19_part2_sample() -> None:
    patterns, designs = day_19.parse(SAMPLE_INPUT)
    assert day_19.solve_part2(patterns, designs) == 16
