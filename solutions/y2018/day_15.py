from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional, Sequence, Tuple


Coordinate = tuple[int, int]


@dataclass(frozen=True)
class UnitTemplate:
    race: str
    position: Coordinate


@dataclass(frozen=True)
class Scenario:
    grid: tuple[str, ...]
    units: tuple[UnitTemplate, ...]


@dataclass
class Unit:
    race: str
    x: int
    y: int
    attack: int = 3
    hp: int = 200
    alive: bool = True

    @property
    def position(self) -> Coordinate:
        return (self.x, self.y)

    def move_to(self, position: Coordinate) -> None:
        self.x, self.y = position


def parse(raw: str) -> Scenario:
    lines = tuple(raw.strip("\n").splitlines())
    units: list[UnitTemplate] = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in ("E", "G"):
                units.append(UnitTemplate(race=char, position=(x, y)))
    return Scenario(grid=lines, units=tuple(units))


NEIGHBORS: tuple[Coordinate, ...] = ((0, -1), (-1, 0), (1, 0), (0, 1))


def reading_order(position: Coordinate) -> tuple[int, int]:
    x, y = position
    return (y, x)


def adjacent(position: Coordinate) -> Iterator[Coordinate]:
    x, y = position
    for dx, dy in NEIGHBORS:
        yield (x + dx, y + dy)


def is_open(grid: Sequence[str], position: Coordinate) -> bool:
    x, y = position
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[y]):
        return False
    return grid[y][x] != "#"


def bfs_next_step(
    grid: Sequence[str],
    start: Coordinate,
    targets: set[Coordinate],
    occupied: set[Coordinate],
) -> Optional[Coordinate]:
    if not targets:
        return None
    from collections import deque

    queue = deque([(start, 0, None)])
    visited = {start}
    found: list[tuple[Coordinate, Coordinate]] = []
    best_distance: Optional[int] = None

    while queue:
        position, distance, first_step = queue.popleft()
        if best_distance is not None and distance > best_distance:
            break
        if position in targets and position != start:
            best_distance = distance
            found.append((position, first_step if first_step is not None else position))
            continue
        for dx, dy in NEIGHBORS:
            next_pos = (position[0] + dx, position[1] + dy)
            if next_pos in visited or next_pos in occupied:
                continue
            if not is_open(grid, next_pos):
                continue
            visited.add(next_pos)
            next_first = first_step if first_step is not None else next_pos
            queue.append((next_pos, distance + 1, next_first))
    if not found:
        return None
    found.sort(key=lambda item: (reading_order(item[0]), reading_order(item[1])))
    return found[0][1]


def simulate(
    scenario: Scenario,
    elf_attack: int = 3,
    stop_on_elf_death: bool = False,
) -> dict[str, int | bool]:
    grid = scenario.grid
    units: list[Unit] = []
    for template in scenario.units:
        attack = elf_attack if template.race == "E" else 3
        units.append(
            Unit(
                race=template.race,
                x=template.position[0],
                y=template.position[1],
                attack=attack,
            )
        )

    rounds_completed = 0
    elf_died = False

    while True:
        units_in_order = sorted(
            (unit for unit in units if unit.alive),
            key=lambda unit: reading_order(unit.position),
        )
        for index, unit in enumerate(units_in_order):
            if not unit.alive:
                continue

            enemies = [u for u in units if u.alive and u.race != unit.race]
            if not enemies:
                total_hp = sum(u.hp for u in units if u.alive)
                return {
                    "rounds": rounds_completed,
                    "total_hp": total_hp,
                    "elf_died": elf_died,
                }

            adjacent_positions = list(adjacent(unit.position))
            adjacent_enemies = [
                enemy for enemy in enemies if enemy.position in adjacent_positions
            ]

            if not adjacent_enemies:
                occupied = {
                    u.position for u in units if u.alive and u is not unit
                }
                target_squares = {
                    pos
                    for enemy in enemies
                    for pos in adjacent(enemy.position)
                    if is_open(grid, pos) and pos not in occupied
                }
                next_step = bfs_next_step(grid, unit.position, target_squares, occupied)
                if next_step is not None:
                    unit.move_to(next_step)
                    adjacent_positions = list(adjacent(unit.position))
                    adjacent_enemies = [
                        enemy
                        for enemy in enemies
                        if enemy.position in adjacent_positions
                    ]

            if adjacent_enemies:
                target = min(
                    adjacent_enemies,
                    key=lambda enemy: (enemy.hp, reading_order(enemy.position)),
                )
                target.hp -= unit.attack
                if target.hp <= 0:
                    target.alive = False
                    if target.race == "E":
                        elf_died = True
                        if stop_on_elf_death:
                            return {"elf_died": True}
                if not any(u.alive and u.race != unit.race for u in units):
                    total_hp = sum(u.hp for u in units if u.alive)
                    remaining_to_act = any(
                        other.alive for other in units_in_order[index + 1 :]
                    )
                    rounds_value = (
                        rounds_completed if remaining_to_act else rounds_completed + 1
                    )
                    return {
                        "rounds": rounds_value,
                        "total_hp": total_hp,
                        "elf_died": elf_died,
                    }

        rounds_completed += 1


def solve_part1(scenario: Scenario) -> int:
    outcome = simulate(scenario)
    rounds = int(outcome["rounds"])
    total_hp = int(outcome["total_hp"])
    return rounds * total_hp


def solve_part2(scenario: Scenario) -> int:
    attack = 4
    while True:
        outcome = simulate(scenario, elf_attack=attack, stop_on_elf_death=True)
        if outcome.get("elf_died"):
            attack += 1
            continue
        rounds = int(outcome["rounds"])
        total_hp = int(outcome["total_hp"])
        return rounds * total_hp


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 15.")
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
