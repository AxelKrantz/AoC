from solutions.y2017 import day_10


def test_sparse_hash_product() -> None:
    lengths = day_10.parse("3,4,1,5")
    result = day_10.solve_part1(lengths, size=5)
    assert result == 12


def test_knot_hash_examples() -> None:
    assert day_10.knot_hash("") == "a2582a3a0e66e6e86e3812dcb672a272"
    assert day_10.knot_hash("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
    assert day_10.knot_hash("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
    assert day_10.knot_hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"
