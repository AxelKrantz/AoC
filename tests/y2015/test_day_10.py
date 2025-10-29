from solutions.y2015 import day_10


def test_look_and_say_sequence() -> None:
    sequence = "1"
    sequence = day_10.look_and_say(sequence)
    assert sequence == "11"
    sequence = day_10.look_and_say(sequence)
    assert sequence == "21"
    assert day_10.iterate("1", 5) == "312211"
