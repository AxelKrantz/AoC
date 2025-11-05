from solutions.y2015 import day_22


def test_sample_battle_minimum_mana() -> None:
    boss = day_22.parse(
        """Hit Points: 13
Damage: 8
"""
    )
    assert (
        day_22.minimal_mana_to_win(
            boss, hard_mode=False, player_hp=10, player_mana=250
        )
        == 226
    )


def test_hard_mode_requires_additional_resources() -> None:
    boss = day_22.parse(
        """Hit Points: 20
Damage: 12
"""
    )
    normal = day_22.minimal_mana_to_win(boss, hard_mode=False)
    hard = day_22.minimal_mana_to_win(boss, hard_mode=True)
    assert hard > normal
