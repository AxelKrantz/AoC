from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence


def parse(raw: str) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        a_str, b_str = line.split()
        left.append(int(a_str))
        right.append(int(b_str))
    return left, right


def solve_part1(left: Sequence[int], right: Sequence[int]) -> int:
    sorted_left = sorted(left)
    sorted_right = sorted(right)
    return sum(abs(a - b) for a, b in zip(sorted_left, sorted_right))


def solve_part2(left: Sequence[int], right: Sequence[int]) -> int:
    from collections import Counter

    counts = Counter(right)
    return sum(value * counts[value] for value in left)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 1.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    left, right = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(left, right)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(left, right)}")


if __name__ == "__main__":
    main()
