from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass
class Group:
    id: int
    army: str
    units: int
    hit_points: int
    attack_damage: int
    attack_type: str
    initiative: int
    weaknesses: set[str]
    immunities: set[str]

    def effective_power(self) -> int:
        return self.units * self.attack_damage

    def copy_with_boost(self, boost: int) -> "Group":
        damage = self.attack_damage + boost if self.army == "Immune System" else self.attack_damage
        return Group(
            id=self.id,
            army=self.army,
            units=self.units,
            hit_points=self.hit_points,
            attack_damage=damage,
            attack_type=self.attack_type,
            initiative=self.initiative,
            weaknesses=set(self.weaknesses),
            immunities=set(self.immunities),
        )


GROUP_PATTERN = re.compile(
    r"(?P<units>\d+) units each with (?P<hp>\d+) hit points(?: \((?P<attrs>[^)]+)\))? "
    r"with an attack that does (?P<damage>\d+) (?P<type>\w+) damage at initiative (?P<initiative>\d+)"
)


def parse_group(line: str, *, group_id: int, army: str) -> Group:
    match = GROUP_PATTERN.fullmatch(line)
    if not match:
        raise ValueError(f"Unable to parse group line: {line!r}")
    units = int(match.group("units"))
    hit_points = int(match.group("hp"))
    damage = int(match.group("damage"))
    attack_type = match.group("type")
    initiative = int(match.group("initiative"))
    weaknesses: set[str] = set()
    immunities: set[str] = set()
    attrs = match.group("attrs")
    if attrs:
        for part in attrs.split(";"):
            part = part.strip()
            if part.startswith("weak to "):
                weaknesses.update(value.strip() for value in part[8:].split(","))
            elif part.startswith("immune to "):
                immunities.update(value.strip() for value in part[10:].split(","))
    return Group(
        id=group_id,
        army=army,
        units=units,
        hit_points=hit_points,
        attack_damage=damage,
        attack_type=attack_type,
        initiative=initiative,
        weaknesses=weaknesses,
        immunities=immunities,
    )


def parse(raw: str) -> List[Group]:
    sections = raw.strip().split("\n\n")
    groups: list[Group] = []
    group_id = 1
    for section in sections:
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        army_name = lines[0].rstrip(":")
        for line in lines[1:]:
            groups.append(parse_group(line, group_id=group_id, army=army_name))
            group_id += 1
    return groups


def potential_damage(attacker: Group, defender: Group) -> int:
    if attacker.attack_type in defender.immunities:
        return 0
    multiplier = 2 if attacker.attack_type in defender.weaknesses else 1
    return attacker.effective_power() * multiplier


def simulate_battle(original_groups: Sequence[Group], boost: int = 0) -> Optional[Tuple[str, int]]:
    groups = [group.copy_with_boost(boost) for group in original_groups]

    while True:
        living_groups = [group for group in groups if group.units > 0]
        armies = {group.army for group in living_groups}
        if len(armies) == 1:
            army = living_groups[0].army
            total_units = sum(group.units for group in living_groups)
            return army, total_units

        target_selection_order = sorted(
            living_groups, key=lambda g: (g.effective_power(), g.initiative), reverse=True
        )

        targeted: set[int] = set()
        assignments: Dict[int, Group] = {}

        for attacker in target_selection_order:
            enemies = [
                enemy
                for enemy in living_groups
                if enemy.army != attacker.army and enemy.id not in targeted and enemy.units > 0
            ]
            enemies.sort(
                key=lambda enemy: (
                    potential_damage(attacker, enemy),
                    enemy.effective_power(),
                    enemy.initiative,
                ),
                reverse=True,
            )
            if not enemies:
                continue
            target = enemies[0]
            if potential_damage(attacker, target) == 0:
                continue
            assignments[attacker.id] = target
            targeted.add(target.id)

        attack_order = sorted(living_groups, key=lambda g: g.initiative, reverse=True)
        total_units_killed = 0

        for attacker in attack_order:
            if attacker.units <= 0:
                continue
            target = assignments.get(attacker.id)
            if not target or target.units <= 0:
                continue
            damage = potential_damage(attacker, target)
            killed = min(target.units, damage // target.hit_points)
            if killed > 0:
                target.units -= killed
                total_units_killed += killed

        if total_units_killed == 0:
            return None


def solve_part1(groups: Sequence[Group]) -> int:
    result = simulate_battle(groups, boost=0)
    if result is None:
        raise RuntimeError("Battle ended in a stalemate for Part 1.")
    _winner, units = result
    return units


def solve_part2(groups: Sequence[Group]) -> int:
    boost = 1
    while True:
        result = simulate_battle(groups, boost)
        if result is not None and result[0] == "Immune System":
            break
        boost *= 2

    low = boost // 2
    high = boost
    winning_units = result[1]
    while low < high:
        mid = (low + high) // 2
        result = simulate_battle(groups, mid)
        if result is not None and result[0] == "Immune System":
            high = mid
            winning_units = result[1]
        else:
            low = mid + 1
    return winning_units


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 24.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    data = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
