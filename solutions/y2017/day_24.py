from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple


Component = Tuple[int, int]


def parse(raw: str) -> List[Component]:
    components: list[Component] = []
    for line in raw.strip().splitlines():
        left, right = line.split("/")
        components.append((int(left), int(right)))
    return components


def solve_part1(components: List[Component]) -> int:
    @lru_cache(maxsize=None)
    def dfs(port: int, used_mask: int) -> int:
        best = 0
        for index, (a, b) in enumerate(components):
            if used_mask & (1 << index):
                continue
            if a == port or b == port:
                next_port = b if a == port else a
                strength = a + b + dfs(next_port, used_mask | (1 << index))
                best = max(best, strength)
        return best

    return dfs(0, 0)


def solve_part2(components: List[Component]) -> int:
    @lru_cache(maxsize=None)
    def dfs(port: int, used_mask: int) -> Tuple[int, int]:
        best_length_strength = (0, 0)
        for index, (a, b) in enumerate(components):
            if used_mask & (1 << index):
                continue
            if a == port or b == port:
                next_port = b if a == port else a
                length, strength = dfs(next_port, used_mask | (1 << index))
                length += 1
                strength += a + b
                if length > best_length_strength[0] or (length == best_length_strength[0] and strength > best_length_strength[1]):
                    best_length_strength = (length, strength)
        return best_length_strength

    return dfs(0, 0)[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 24.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    components = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(components)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(components)}")


if __name__ == "__main__":
    main()
