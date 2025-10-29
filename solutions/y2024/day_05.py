from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Iterable, List, Tuple

Rule = Tuple[int, int]
Update = List[int]


def parse(raw: str) -> tuple[list[Rule], list[Update]]:
    rules_block, updates_block = raw.strip().split("\n\n", 1)
    rules: list[Rule] = []
    for line in rules_block.splitlines():
        if line.strip():
            left, right = line.split("|")
            rules.append((int(left), int(right)))
    updates: list[Update] = []
    for line in updates_block.splitlines():
        if line.strip():
            updates.append([int(value) for value in line.split(",")])
    return rules, updates


def is_valid_update(update: Update, rules: Iterable[Rule]) -> bool:
    positions = {value: index for index, value in enumerate(update)}
    for before, after in rules:
        if before in positions and after in positions:
            if positions[before] > positions[after]:
                return False
    return True


def order_update(update: Update, rules: Iterable[Rule]) -> Update:
    nodes = set(update)
    adjacency: dict[int, set[int]] = {node: set() for node in nodes}
    indegree: dict[int, int] = {node: 0 for node in nodes}

    for before, after in rules:
        if before in nodes and after in nodes:
            if after not in adjacency[before]:
                adjacency[before].add(after)
                indegree[after] += 1

    queue = deque(sorted((node for node in nodes if indegree[node] == 0), key=update.index))
    ordered: list[int] = []
    while queue:
        node = queue.popleft()
        ordered.append(node)
        for neighbor in sorted(adjacency[node], key=update.index):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered) != len(update):
        raise ValueError("Cycle detected when ordering update.")
    return ordered


def middle_value(update: Update) -> int:
    return update[len(update) // 2]


def solve_part1(rules: list[Rule], updates: list[Update]) -> int:
    return sum(middle_value(update) for update in updates if is_valid_update(update, rules))


def solve_part2(rules: list[Rule], updates: list[Update]) -> int:
    total = 0
    for update in updates:
        if not is_valid_update(update, rules):
            corrected = order_update(update, rules)
            total += middle_value(corrected)
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 5.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    rules, updates = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(rules, updates)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(rules, updates)}")


if __name__ == "__main__":
    main()
