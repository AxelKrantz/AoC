from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path
from typing import Iterable


def parse(raw: str) -> list[int]:
    return [int(line) for line in raw.strip().splitlines() if line]


def count_combinations(containers: list[int], target: int) -> int:
    total = 0
    for r in range(1, len(containers) + 1):
        for combo in combinations(containers, r):
            if sum(combo) == target:
                total += 1
    return total


def minimal_container_combinations(containers: list[int], target: int) -> int:
    for r in range(1, len(containers) + 1):
        count = 0
        for combo in combinations(containers, r):
            if sum(combo) == target:
                count += 1
        if count:
            return count
    return 0


def solve_part1(containers: list[int], target: int = 150) -> int:
    return count_combinations(containers, target)


def solve_part2(containers: list[int], target: int = 150) -> int:
    return minimal_container_combinations(containers, target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 17.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--target", type=int, default=150)
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    containers = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(containers, args.target)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(containers, args.target)}")


if __name__ == "__main__":
    main()
