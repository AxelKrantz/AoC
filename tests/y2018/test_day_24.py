from textwrap import dedent

from solutions.y2018 import day_24


SAMPLE_INPUT = dedent(
    """\
    Immune System:
    17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

    Infection:
    801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
    4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
    """
)


def test_part1_example() -> None:
    groups = day_24.parse(SAMPLE_INPUT)
    assert day_24.solve_part1(groups) == 5216


def test_part2_example() -> None:
    groups = day_24.parse(SAMPLE_INPUT)
    assert day_24.solve_part2(groups) == 51
