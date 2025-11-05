from solutions.y2015 import day_21


def test_battle_outcome_basic() -> None:
    player = day_21.Combatant(hit_points=8, damage=5, armor=5)
    boss = day_21.Combatant(hit_points=12, damage=7, armor=2)
    assert day_21.battle_outcome(player, boss) is True
    weaker_player = day_21.Combatant(hit_points=8, damage=3, armor=1)
    assert day_21.battle_outcome(weaker_player, boss) is False


def test_optimal_costs_against_sample_boss() -> None:
    boss = day_21.parse(
        """Hit Points: 20
Damage: 7
Armor: 5
"""
    )
    assert day_21.solve_part1(boss) == 39
    assert day_21.solve_part2(boss) == 78
