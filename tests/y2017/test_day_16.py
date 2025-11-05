from solutions.y2017 import day_16


SAMPLE = "s1,x3/4,pe/b"


def test_permutation_promenade_example() -> None:
    moves = day_16.parse(SAMPLE)
    assert day_16.solve_part1(moves, programs="abcde") == "baedc"
    assert day_16.solve_part2(moves, programs="abcde", iterations=2) == "ceadb"
