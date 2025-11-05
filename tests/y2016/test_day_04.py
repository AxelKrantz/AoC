from solutions.y2016 import day_04


EXAMPLE = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""


def test_sector_id_sum_for_real_rooms() -> None:
    rooms = day_04.parse(EXAMPLE)
    assert day_04.solve_part1(rooms) == 1514


def test_decrypts_northpole_storage() -> None:
    room = day_04.Room(name="qzmt-zixmtkozy-ivhz", sector_id=343, checksum="zimth")
    assert day_04.decrypt(room) == "very encrypted name"
