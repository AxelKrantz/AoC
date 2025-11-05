from solutions.y2016 import day_09


def test_decompression_lengths_part1() -> None:
    assert day_09.solve_part1("ADVENT") == 6
    assert day_09.solve_part1("A(1x5)BC") == 7
    assert day_09.solve_part1("(3x3)XYZ") == 9
    assert day_09.solve_part1("A(2x2)BCD(2x2)EFG") == 11
    assert day_09.solve_part1("(6x1)(1x3)A") == 6
    assert day_09.solve_part1("X(8x2)(3x3)ABCY") == 18


def test_decompression_lengths_part2() -> None:
    assert day_09.solve_part2("(3x3)XYZ") == 9
    assert day_09.solve_part2("X(8x2)(3x3)ABCY") == 20
    assert day_09.solve_part2("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
    assert day_09.solve_part2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445
