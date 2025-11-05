from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import inf
from pathlib import Path
from typing import Dict, Tuple


@dataclass(frozen=True)
class Boss:
    hit_points: int
    damage: int


Spell = Tuple[str, int, int, int, int, int]

SPELLS: tuple[Spell, ...] = (
    ("Magic Missile", 53, 4, 0, 0, 0),
    ("Drain", 73, 2, 2, 0, 0),
    ("Shield", 113, 0, 0, 6, 0),
    ("Poison", 173, 0, 0, 0, 6),
    ("Recharge", 229, 0, 0, 0, 0),
)


def parse(raw: str) -> Boss:
    stats: dict[str, int] = {}
    for line in raw.strip().splitlines():
        key, value = line.split(": ")
        stats[key] = int(value)
    return Boss(hit_points=stats["Hit Points"], damage=stats["Damage"])


def minimal_mana_to_win(
    boss: Boss, *, hard_mode: bool, player_hp: int = 50, player_mana: int = 500
) -> int:
    best = inf
    seen: Dict[Tuple[int, int, int, int, int, int], int] = {}

    def dfs(
        player_hp: int,
        player_mana: int,
        boss_hp: int,
        shield_timer: int,
        poison_timer: int,
        recharge_timer: int,
        mana_spent: int,
    ) -> None:
        nonlocal best

        if mana_spent >= best:
            return

        state = (
            player_hp,
            player_mana,
            boss_hp,
            shield_timer,
            poison_timer,
            recharge_timer,
        )
        previous = seen.get(state)
        if previous is not None and previous <= mana_spent:
            return
        seen[state] = mana_spent

        hp = player_hp
        mana = player_mana
        boss_current = boss_hp
        shield = shield_timer
        poison = poison_timer
        recharge = recharge_timer

        if hard_mode:
            hp -= 1
            if hp <= 0:
                return

        if shield > 0:
            shield -= 1
        if poison > 0:
            boss_current -= 3
            poison -= 1
        if recharge > 0:
            mana += 101
            recharge -= 1
        if boss_current <= 0:
            best = min(best, mana_spent)
            return

        for name, cost, damage, heal, shield_duration, poison_duration in SPELLS:
            if mana < cost:
                continue
            if name == "Shield" and shield > 0:
                continue
            if name == "Poison" and poison > 0:
                continue
            if name == "Recharge" and recharge > 0:
                continue

            new_hp = hp + heal
            new_mana = mana - cost
            new_boss_hp = boss_current - damage
            new_shield = shield
            new_poison = poison
            new_recharge = recharge

            if name == "Shield":
                new_shield = shield_duration
            elif name == "Poison":
                new_poison = poison_duration
            elif name == "Recharge":
                new_recharge = 5

            new_mana_spent = mana_spent + cost

            if new_boss_hp <= 0:
                best = min(best, new_mana_spent)
                continue

            if new_shield > 0:
                new_shield -= 1
                armor_boss = 7
            else:
                armor_boss = 0

            if new_poison > 0:
                new_boss_hp -= 3
                new_poison -= 1

            if new_recharge > 0:
                new_mana += 101
                new_recharge -= 1

            if new_boss_hp <= 0:
                best = min(best, new_mana_spent)
                continue

            damage_to_player = max(1, boss.damage - armor_boss)
            next_hp = new_hp - damage_to_player
            if next_hp <= 0:
                continue

            dfs(
                next_hp,
                new_mana,
                new_boss_hp,
                new_shield,
                new_poison,
                new_recharge,
                new_mana_spent,
            )

    dfs(player_hp, player_mana, boss.hit_points, 0, 0, 0, 0)
    if best is inf:
        raise ValueError("No winning strategy found.")
    return int(best)


def solve_part1(boss: Boss) -> int:
    return minimal_mana_to_win(boss, hard_mode=False)


def solve_part2(boss: Boss) -> int:
    return minimal_mana_to_win(boss, hard_mode=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 22.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    boss = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(boss)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(boss)}")


if __name__ == "__main__":
    main()
