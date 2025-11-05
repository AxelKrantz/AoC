from solutions.y2016 import day_05


def test_password_generation_examples() -> None:
    door_id = day_05.parse("abc")
    part1, part2 = day_05.find_hashes(door_id)
    assert part1 == "18f47a30"
    assert part2 == "05ace8e3"
