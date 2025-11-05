from solutions.y2017 import day_07


SAMPLE = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""


def test_recursive_circus_example() -> None:
    programs = day_07.parse(SAMPLE)
    assert day_07.solve_part1(programs) == "tknk"
    assert day_07.solve_part2(programs) == 60
