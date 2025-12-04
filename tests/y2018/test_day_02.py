from solutions.y2018 import day_02


def test_part1_examples() -> None:
    inputs = day_02.parse(
        "\n".join(
            [
                "abcdef",
                "bababc",
                "abbcde",
                "abcccd",
                "aabcdd",
                "abcdee",
                "ababab",
            ]
        )
    )
    assert day_02.solve_part1(inputs) == 12


def test_part2_examples() -> None:
    inputs = day_02.parse(
        "\n".join(
            [
                "abcde",
                "fghij",
                "klmno",
                "pqrst",
                "fguij",
                "axcye",
                "wvxyz",
            ]
        )
    )
    assert day_02.solve_part2(inputs) == "fgij"

