from solutions.y2024 import day_23


SAMPLE_INPUT = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def test_day23_part1_sample() -> None:
    graph = day_23.parse(SAMPLE_INPUT)
    assert day_23.solve_part1(graph) == 7


def test_day23_part2_sample() -> None:
    graph = day_23.parse(SAMPLE_INPUT)
    assert day_23.solve_part2(graph) == "co,de,ka,ta"
