from solutions.y2017 import day_11


def test_hex_path_distances() -> None:
    assert day_11.solve_part1(day_11.parse("ne,ne,ne")) == 3
    assert day_11.solve_part1(day_11.parse("ne,ne,sw,sw")) == 0
    assert day_11.solve_part1(day_11.parse("ne,ne,s,s")) == 2
    assert day_11.solve_part1(day_11.parse("se,sw,se,sw,sw")) == 3


def test_hex_path_furthest_distance() -> None:
    assert day_11.solve_part2(day_11.parse("ne,ne,ne")) == 3
    assert day_11.solve_part2(day_11.parse("ne,ne,sw,sw")) == 2
    assert day_11.solve_part2(day_11.parse("ne,ne,s,s")) == 2
