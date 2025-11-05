from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Dict, Iterable, Set


def parse(raw: str) -> Dict[int, Set[int]]:
    graph: Dict[int, Set[int]] = {}
    for line in raw.strip().splitlines():
        left, right = line.split(" <-> ")
        node = int(left.strip())
        neighbors = {int(value.strip()) for value in right.split(",")}
        graph.setdefault(node, set()).update(neighbors)
        for neighbor in neighbors:
            graph.setdefault(neighbor, set()).add(node)
    return graph


def connected_component(graph: Dict[int, Set[int]], start: int) -> Set[int]:
    visited: Set[int] = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        queue.extend(graph.get(node, set()))
    return visited


def count_groups(graph: Dict[int, Set[int]]) -> int:
    remaining = set(graph.keys())
    groups = 0
    while remaining:
        start = next(iter(remaining))
        component = connected_component(graph, start)
        remaining -= component
        groups += 1
    return groups


def solve_part1(graph: Dict[int, Set[int]]) -> int:
    return len(connected_component(graph, 0))


def solve_part2(graph: Dict[int, Set[int]]) -> int:
    return count_groups(graph)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 12.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    graph = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(graph)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(graph)}")


if __name__ == "__main__":
    main()
