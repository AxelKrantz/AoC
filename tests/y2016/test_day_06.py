from solutions.y2016 import day_06


SAMPLE = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""


def test_repetition_code_messages() -> None:
    rows = day_06.parse(SAMPLE)
    assert day_06.solve_part1(rows) == "easter"
    assert day_06.solve_part2(rows) == "advent"
