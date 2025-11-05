from solutions.y2016 import day_17


def test_shortest_paths_examples() -> None:
    assert day_17.solve_part1("ihgpwlah") == "DDRRRD"
    assert day_17.solve_part1("kglvqrro") == "DDUDRLRRUDRD"


def test_longest_path_example() -> None:
    assert day_17.solve_part2("ihgpwlah") == 370
