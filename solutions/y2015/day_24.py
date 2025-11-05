from __future__ import annotations

import argparse
import functools
import math
from itertools import combinations
from pathlib import Path
from typing import Iterable, Tuple


def parse(raw: str) -> tuple[int, ...]:
    return tuple(int(line) for line in raw.strip().splitlines() if line)


def quantum_entanglement(weights: Iterable[int]) -> int:
    product = 1
    for weight in weights:
        product *= weight
    return product


def find_best_group(weights: tuple[int, ...], groups: int) -> int:
    total_weight = sum(weights)
    target = total_weight // groups

    @functools.lru_cache(maxsize=None)
    def can_partition(remaining: tuple[int, ...], partition_groups: int) -> bool:
        if partition_groups == 1:
            return sum(remaining) == target
        length = len(remaining)
        for size in range(1, length + 1):
            for combo in combinations(remaining, size):
                if sum(combo) != target:
                    continue
                leftover = list(remaining)
                for weight in combo:
                    leftover.remove(weight)
                if can_partition(tuple(sorted(leftover)), partition_groups - 1):
                    return True
        return False

    weights_sorted = tuple(sorted(weights, reverse=True))

    for size in range(1, len(weights_sorted) + 1):
        best_qe = math.inf
        for combo in combinations(weights_sorted, size):
            if sum(combo) != target:
                continue
            leftover = list(weights_sorted)
            for weight in combo:
                leftover.remove(weight)
            if can_partition(tuple(sorted(leftover)), groups - 1):
                best_qe = min(best_qe, quantum_entanglement(combo))
        if best_qe != math.inf:
            return int(best_qe)
    raise ValueError("No valid partition found.")


def solve_part1(weights: tuple[int, ...]) -> int:
    return find_best_group(weights, groups=3)


def solve_part2(weights: tuple[int, ...]) -> int:
    return find_best_group(weights, groups=4)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 24.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    weights = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(weights)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(weights)}")


if __name__ == "__main__":
    main()
