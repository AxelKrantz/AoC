import pytest

from solutions.y2015 import day_02


def test_parse_dimensions() -> None:
    boxes = day_02.parse("2x3x4\n1x1x10\n")
    assert boxes == [(2, 3, 4), (1, 1, 10)]


@pytest.mark.parametrize(
    ("dims", "expected"),
    [
        ((2, 3, 4), 58),
        ((1, 1, 10), 43),
    ],
)
def test_surface_area_examples(dims, expected) -> None:
    assert day_02.surface_area_with_slack(dims) == expected


@pytest.mark.parametrize(
    ("dims", "expected"),
    [
        ((2, 3, 4), 34),
        ((1, 1, 10), 14),
    ],
)
def test_ribbon_examples(dims, expected) -> None:
    assert day_02.ribbon_length(dims) == expected
