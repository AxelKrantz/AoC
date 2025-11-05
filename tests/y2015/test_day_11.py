from solutions.y2015 import day_11


def test_next_password_examples() -> None:
    assert day_11.next_password("abcdefgh") == "abcdffaa"
    assert day_11.next_password("ghijklmn") == "ghjaabcc"


def test_part2_uses_successive_passwords() -> None:
    assert day_11.solve_part2("abcdefgh") == "abcdffbb"
