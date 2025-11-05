from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Iterable


PLAYER_HIT_POINTS = 100


@dataclass(frozen=True)
class Equipment:
    cost: int
    damage: int
    armor: int


WEAPONS = [
    Equipment(8, 4, 0),
    Equipment(10, 5, 0),
    Equipment(25, 6, 0),
    Equipment(40, 7, 0),
    Equipment(74, 8, 0),
]

ARMORS = [
    Equipment(0, 0, 0),
    Equipment(13, 0, 1),
    Equipment(31, 0, 2),
    Equipment(53, 0, 3),
    Equipment(75, 0, 4),
    Equipment(102, 0, 5),
]

RINGS = [
    Equipment(25, 1, 0),
    Equipment(50, 2, 0),
    Equipment(100, 3, 0),
    Equipment(20, 0, 1),
    Equipment(40, 0, 2),
    Equipment(80, 0, 3),
]


@dataclass(frozen=True)
class Combatant:
    hit_points: int
    damage: int
    armor: int


def parse(raw: str) -> Combatant:
    stats: dict[str, int] = {}
    for line in raw.strip().splitlines():
        name, value = line.split(": ")
        stats[name] = int(value)
    return Combatant(
        hit_points=stats["Hit Points"],
        damage=stats["Damage"],
        armor=stats["Armor"],
    )


def turns_to_defeat(attacker: Combatant, defender: Combatant) -> int:
    damage = max(1, attacker.damage - defender.armor)
    return ceil(defender.hit_points / damage)


def battle_outcome(player: Combatant, boss: Combatant) -> bool:
    player_turns = turns_to_defeat(player, boss)
    boss_turns = turns_to_defeat(boss, player)
    return player_turns <= boss_turns


def equipment_loadouts() -> Iterable[Equipment]:
    for weapon in WEAPONS:
        for armor in ARMORS:
            ring_choices = [()]
            ring_choices.extend(itertools.combinations(RINGS, 1))
            ring_choices.extend(itertools.combinations(RINGS, 2))
            for rings in ring_choices:
                cost = weapon.cost + armor.cost + sum(r.cost for r in rings)
                damage = weapon.damage + armor.damage + sum(r.damage for r in rings)
                protection = weapon.armor + armor.armor + sum(r.armor for r in rings)
                yield Equipment(cost, damage, protection)


def best_cost(boss: Combatant) -> tuple[int, int]:
    cheapest_win = float("inf")
    priciest_loss = 0
    for loadout in equipment_loadouts():
        player = Combatant(PLAYER_HIT_POINTS, loadout.damage, loadout.armor)
        if battle_outcome(player, boss):
            cheapest_win = min(cheapest_win, loadout.cost)
        else:
            priciest_loss = max(priciest_loss, loadout.cost)
    return int(cheapest_win), int(priciest_loss)


def solve_part1(boss: Combatant) -> int:
    win_cost, _ = best_cost(boss)
    return win_cost


def solve_part2(boss: Combatant) -> int:
    _, loss_cost = best_cost(boss)
    return loss_cost


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 21.")
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
