from __future__ import annotations

import argparse
from collections import deque, defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, Iterator, Set, Tuple

Point = tuple[int, int]


def parse(raw: str) -> str:
    return raw.strip()


DIRECTIONS: Dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}


def build_graph(regex: str) -> DefaultDict[Point, Set[Point]]:
    graph: DefaultDict[Point, Set[Point]] = defaultdict(set)
    stack: list[tuple[Set[Point], Set[Point]]] = []
    current_positions: Set[Point] = {(0, 0)}
    for char in regex.strip("^$"):
        if char in DIRECTIONS:
            dx, dy = DIRECTIONS[char]
            next_positions: Set[Point] = set()
            for (x, y) in current_positions:
                nx, ny = x + dx, y + dy
                graph[(x, y)].add((nx, ny))
                graph[(nx, ny)].add((x, y))
                next_positions.add((nx, ny))
            current_positions = next_positions
        elif char == "(":
            stack.append((current_positions.copy(), set()))
        elif char == "|":
            start_positions, collected = stack[-1]
            collected.update(current_positions)
            current_positions = start_positions.copy()
        elif char == ")":
            start_positions, collected = stack.pop()
            collected.update(current_positions)
            current_positions = collected
        else:
            raise ValueError(f"Unexpected character in regex: {char!r}")
    return graph


def distances(graph: DefaultDict[Point, Set[Point]], start: Point = (0, 0)) -> Dict[Point, int]:
    dist: Dict[Point, int] = {start: 0}
    queue = deque([start])
    while queue:
        point = queue.popleft()
        for neighbor in graph[point]:
            if neighbor not in dist:
                dist[neighbor] = dist[point] + 1
                queue.append(neighbor)
    return dist


def solve_part1(regex: str) -> int:
    graph = build_graph(regex)
    dist = distances(graph)
    return max(dist.values())


def solve_part2(regex: str, threshold: int = 1000) -> int:
    graph = build_graph(regex)
    dist = distances(graph)
    return sum(1 for value in dist.values() if value >= threshold)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 20.")
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
