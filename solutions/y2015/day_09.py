from __future__ import annotations

import argparse
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, Tuple

Route = Tuple[str, str, int]


def parse(raw: str) -> list[Route]:
    routes: list[Route] = []
    for line in raw.splitlines():
        if not line:
            continue
        left, _, dist_str = line.partition(" = ")
        start, _, end = left.partition(" to ")
        routes.append((start, end, int(dist_str)))
    return routes


def build_graph(routes: Iterable[Route]) -> dict[str, dict[str, int]]:
    graph: dict[str, dict[str, int]] = {}
    for start, end, distance in routes:
        graph.setdefault(start, {})[end] = distance
        graph.setdefault(end, {})[start] = distance
    return graph


def compute_distances(graph: Dict[str, Dict[str, int]]) -> tuple[int, int]:
    cities = list(graph.keys())
    shortest = None
    longest = None
    for order in permutations(cities):
        distance = 0
        valid = True
        for a, b in zip(order, order[1:]):
            if b not in graph[a]:
                valid = False
                break
            distance += graph[a][b]
        if not valid:
            continue
        if shortest is None or distance < shortest:
            shortest = distance
        if longest is None or distance > longest:
            longest = distance
    if shortest is None or longest is None:
        raise ValueError("No valid route found.")
    return shortest, longest


def solve_part1(routes: Iterable[Route]) -> int:
    graph = build_graph(routes)
    shortest, _ = compute_distances(graph)
    return shortest


def solve_part2(routes: Iterable[Route]) -> int:
    graph = build_graph(routes)
    _, longest = compute_distances(graph)
    return longest


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 9.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    routes = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(routes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(routes)}")


if __name__ == "__main__":
    main()
