import pytest

from solutions.y2015 import day_01


@pytest.mark.parametrize(
    "sequence, expected",
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        (")())())", -3),
        ("))(((((", 3),
    ],
)
def test_part1_samples(sequence: str, expected: int) -> None:
    assert day_01.solve_part1(sequence) == expected


@pytest.mark.parametrize(
    "sequence, expected",
    [
        (")", 1),
        ("()())", 5),
    ],
)
def test_part2_samples(sequence: str, expected: int) -> None:
    assert day_01.solve_part2(sequence) == expected
