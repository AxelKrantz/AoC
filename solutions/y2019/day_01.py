from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


def parse(raw: str) -> list[int]:
    return [int(line) for line in raw.strip().splitlines() if line.strip()]


def fuel_required(mass: int) -> int:
    return max(mass // 3 - 2, 0)


def fuel_with_additional(mass: int) -> int:
    total = 0
    additional = fuel_required(mass)
    while additional > 0:
        total += additional
        additional = fuel_required(additional)
    return total


def solve_part1(masses: Iterable[int]) -> int:
    return sum(fuel_required(mass) for mass in masses)


def solve_part2(masses: Iterable[int]) -> int:
    return sum(fuel_with_additional(mass) for mass in masses)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2019 Day 1.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    masses = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(masses)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(masses)}")


if __name__ == "__main__":
    main()

