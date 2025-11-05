from solutions.y2015 import day_25


def test_code_sequence_matches_examples() -> None:
    assert day_25.compute_code(1, 1) == 20151125
    assert day_25.compute_code(2, 1) == 31916031
    assert day_25.compute_code(1, 2) == 18749137


def test_parse_extracts_row_and_column() -> None:
    raw = "Enter the code at row 4, column 2."
    assert day_25.parse(raw) == (4, 2)
