from solutions.y2015 import day_04


def test_examples_part1() -> None:
    assert day_04.find_lowest_with_prefix("abcdef", "00000") == 609043
    assert day_04.find_lowest_with_prefix("pqrstuv", "00000") == 1048970
