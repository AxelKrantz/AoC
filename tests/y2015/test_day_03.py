import pytest

from solutions.y2015 import day_03


@pytest.mark.parametrize(
    ("instructions", "expected"),
    [
        (">", 2),
        ("^>v<", 4),
        ("^v^v^v^v^v", 2),
    ],
)
def test_part1_examples(instructions: str, expected: int) -> None:
    assert day_03.solve_part1(instructions) == expected


@pytest.mark.parametrize(
    ("instructions", "expected"),
    [
        ("^v", 3),
        ("^>v<", 3),
        ("^v^v^v^v^v", 11),
    ],
)
def test_part2_examples(instructions: str, expected: int) -> None:
    assert day_03.solve_part2(instructions) == expected
