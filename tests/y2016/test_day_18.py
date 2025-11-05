from solutions.y2016 import day_18


def test_trap_tile_generation_example() -> None:
    first_row = day_18.parse(".^^.^.^^^^")
    assert day_18.safe_tiles(first_row, 10) == 38
