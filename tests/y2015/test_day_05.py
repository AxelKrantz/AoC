import pytest

from solutions.y2015 import day_05


@pytest.mark.parametrize(
    ("word", "is_nice"),
    [
        ("ugknbfddgicrmopn", True),
        ("aaa", True),
        ("jchzalrnumimnmhp", False),
        ("haegwjzuvuyypxyu", False),
        ("dvszwmarrgswjxmb", False),
    ],
)
def test_part1_examples(word: str, is_nice: bool) -> None:
    assert day_05.is_nice_part1(word) is is_nice


@pytest.mark.parametrize(
    ("word", "is_nice"),
    [
        ("qjhvhtzxzqqjkmpb", True),
        ("xxyxx", True),
        ("uurcxstgmygtbstg", False),
        ("ieodomkazucvgmuy", False),
    ],
)
def test_part2_examples(word: str, is_nice: bool) -> None:
    assert day_05.is_nice_part2(word) is is_nice
