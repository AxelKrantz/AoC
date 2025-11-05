from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple


def parse(raw: str) -> list[int]:
    return [int(value) for value in raw.strip().split()]


def redistribute(banks: list[int]) -> None:
    max_blocks = max(banks)
    index = banks.index(max_blocks)
    banks[index] = 0
    position = index
    for _ in range(max_blocks):
        position = (position + 1) % len(banks)
        banks[position] += 1


def reallocation_cycles(banks: list[int]) -> Tuple[int, int]:
    seen: dict[tuple[int, ...], int] = {}
    cycles = 0
    configuration = tuple(banks)
    while configuration not in seen:
        seen[configuration] = cycles
        redistribute(banks)
        cycles += 1
        configuration = tuple(banks)
    loop_size = cycles - seen[configuration]
    return cycles, loop_size


def solve_part1(banks: list[int]) -> int:
    cycles, _ = reallocation_cycles(banks[:])
    return cycles


def solve_part2(banks: list[int]) -> int:
    _, loop_size = reallocation_cycles(banks[:])
    return loop_size


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 6.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    banks = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(banks)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(banks)}")


if __name__ == "__main__":
    main()
