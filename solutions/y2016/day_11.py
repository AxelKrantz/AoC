from __future__ import annotations

import argparse
import collections
import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, Dict, Iterable, Iterator, List, Sequence, Set, Tuple


@dataclass(frozen=True)
class Facility:
    generators: Dict[str, int]
    microchips: Dict[str, int]


Item = Tuple[int, int]  # (generator_floor, microchip_floor)
State = Tuple[int, Tuple[Item, ...]]  # elevator floor, sorted items


def parse(raw: str) -> Facility:
    generators: Dict[str, int] = {}
    microchips: Dict[str, int] = {}
    for floor_index, line in enumerate(raw.strip().splitlines()):
        floor = floor_index + 1
        for match in re.finditer(r"(\w+)-compatible microchip", line):
            microchips[match.group(1)] = floor
        for match in re.finditer(r"(\w+) generator", line):
            generators[match.group(1)] = floor
    return Facility(generators=generators, microchips=microchips)


def canonical_state(elevator: int, items: Sequence[Item]) -> State:
    normalized = tuple(sorted(items))
    return elevator, normalized


def make_initial_state(facility: Facility) -> State:
    elements = sorted(set(facility.generators) | set(facility.microchips))
    items: list[Item] = []
    for element in elements:
        gen_floor = facility.generators[element]
        chip_floor = facility.microchips[element]
        items.append((gen_floor, chip_floor))
    return canonical_state(1, items)


def is_state_safe(items: Sequence[Item]) -> bool:
    generators_by_floor: Dict[int, Set[int]] = collections.defaultdict(set)
    chips_by_floor: Dict[int, Set[int]] = collections.defaultdict(set)

    for index, (gen_floor, chip_floor) in enumerate(items):
        generators_by_floor[gen_floor].add(index)
        chips_by_floor[chip_floor].add(index)

    for floor, chips in chips_by_floor.items():
        gens = generators_by_floor.get(floor)
        if not gens:
            continue
        for chip_index in chips:
            gen_floor, _ = items[chip_index]
            if gen_floor != floor:
                return False
    return True


def neighbours(state: State) -> Iterator[State]:
    elevator, items = state
    items_list = list(items)
    components: list[Tuple[str, int]] = []
    for index, (gen, chip) in enumerate(items_list):
        if gen == elevator:
            components.append(("G", index))
        if chip == elevator:
            components.append(("M", index))

    for direction in (-1, 1):
        next_floor = elevator + direction
        if not (1 <= next_floor <= 4):
            continue

        if direction == -1 and not any(
            floor < elevator
            for pair in items_list
            for floor in pair
        ):
            continue

        for combo_size in (2, 1):
            for move in itertools.combinations(components, combo_size):
                new_items = update_items(items_list, move, next_floor)
                if is_state_safe(new_items):
                    yield canonical_state(next_floor, new_items)


def update_items(
    items: Sequence[Item], move: Sequence[Tuple[str, int]], next_floor: int
) -> List[Item]:
    updated = [list(pair) for pair in items]
    for item_type, index in move:
        if item_type == "G":
            updated[index][0] = next_floor
        else:
            updated[index][1] = next_floor
    result: List[Item] = [tuple(pair) for pair in updated]  # type: ignore[list-item]
    return result


def bfs(start: State) -> int:
    queue: Deque[Tuple[State, int]] = collections.deque([(start, 0)])
    seen: set[State] = {start}
    goal_items = tuple((4, 4) for _ in start[1])

    while queue:
        state, steps = queue.popleft()
        elevator, items = state
        if items == goal_items:
            return steps
        for next_state in neighbours(state):
            if not next_state:
                continue
            if next_state in seen:
                continue
            seen.add(next_state)
            queue.append((next_state, steps + 1))
    raise ValueError("No solution found.")


def solve(facility: Facility, extra_pairs: Iterable[str] | None = None) -> int:
    generators = facility.generators.copy()
    microchips = facility.microchips.copy()
    if extra_pairs:
        for element in extra_pairs:
            generators[element] = 1
            microchips[element] = 1
    start = make_initial_state(Facility(generators, microchips))
    return bfs(start)


def solve_part1(facility: Facility) -> int:
    return solve(facility)


def solve_part2(facility: Facility) -> int:
    return solve(facility, extra_pairs=("elerium", "dilithium"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 11.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    facility = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(facility)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(facility)}")


if __name__ == "__main__":
    main()
