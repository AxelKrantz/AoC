from solutions.y2018 import day_14


def test_part1_examples() -> None:
    assert day_14.solve_part1("9") == "5158916779"
    assert day_14.solve_part1("5") == "0124515891"
    assert day_14.solve_part1("18") == "9251071085"
    assert day_14.solve_part1("2018") == "5941429882"


def test_part2_examples() -> None:
    assert day_14.solve_part2("51589") == 9
    assert day_14.solve_part2("01245") == 5
    assert day_14.solve_part2("92510") == 18
    assert day_14.solve_part2("59414") == 2018

