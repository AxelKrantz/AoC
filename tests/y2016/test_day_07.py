from solutions.y2016 import day_07


SAMPLE = """\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""

SAMPLE_SSL = """\
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
"""


def test_tls_support_detection() -> None:
    addresses = day_07.parse(SAMPLE)
    assert day_07.solve_part1(addresses) == 2


def test_ssl_support_detection() -> None:
    addresses = day_07.parse(SAMPLE_SSL)
    assert day_07.solve_part2(addresses) == 3
