from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


def parse(raw: str) -> Dict[str, Set[str]]:
    graph: Dict[str, Set[str]] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split("-")
        graph.setdefault(left, set()).add(right)
        graph.setdefault(right, set()).add(left)
    return graph


def count_triangles_with_t(graph: Dict[str, Set[str]]) -> int:
    count = 0
    vertices = sorted(graph.keys())
    for i, a in enumerate(vertices):
        neighbors_a = graph[a]
        for b in sorted(neighbors_a):
            if b <= a:
                continue
            common = neighbors_a & graph[b]
            for c in sorted(common):
                if c <= b:
                    continue
                if any(name.startswith("t") for name in (a, b, c)):
                    count += 1
    return count


def largest_clique(graph: Dict[str, Set[str]]) -> List[str]:
    best_clique: List[str] = []

    def bronk(r: Set[str], p: Set[str], x: Set[str]) -> None:
        nonlocal best_clique
        if not p and not x:
            if len(r) > len(best_clique):
                best_clique = sorted(r)
            return
        # Pivot strategy
        if p or x:
            u = max((p | x), key=lambda vertex: len(graph[vertex]))
            for v in list(p - graph[u]):
                bronk(r | {v}, p & graph[v], x & graph[v])
                p.remove(v)
                x.add(v)

    vertices = set(graph.keys())
    bronk(set(), vertices, set())
    return best_clique


def solve_part1(graph: Dict[str, Set[str]]) -> int:
    return count_triangles_with_t(graph)


def solve_part2(graph: Dict[str, Set[str]]) -> str:
    clique = largest_clique(graph)
    return ",".join(clique)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 23.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    graph = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(graph)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(graph)}")


if __name__ == "__main__":
    main()
