from solutions.y2017 import day_04


PART1_SAMPLE = """\
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
"""

PART2_SAMPLE = """\
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
"""


def test_passphrase_validation_part1() -> None:
    passphrases = day_04.parse(PART1_SAMPLE)
    assert day_04.solve_part1(passphrases) == 2


def test_passphrase_validation_part2() -> None:
    passphrases = day_04.parse(PART2_SAMPLE)
    assert day_04.solve_part2(passphrases) == 3
