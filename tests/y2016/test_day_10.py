from solutions.y2016 import day_10


SAMPLE = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""


def test_bot_comparison_detection() -> None:
    values, bots = day_10.parse(SAMPLE)
    assert day_10.solve_part1(values, bots, target_low=2, target_high=5) == 2
    assert day_10.solve_part2(values, bots) == 30
