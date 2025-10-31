from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

Stones = tuple[int, ...]


def parse(raw: str) -> Stones:
    return tuple(int(value) for value in raw.split())


@lru_cache(maxsize=None)
def blink_result(value: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if value == 0:
        return blink_result(1, blinks - 1)
    digits = str(value)
    if len(digits) % 2 == 0:
        half = len(digits) // 2
        left = int(digits[: half])
        right = int(digits[half:])
        return blink_result(left, blinks - 1) + blink_result(right, blinks - 1)
    return blink_result(value * 2024, blinks - 1)


def blink_total(stones: Sequence[int], blinks: int) -> int:
    return sum(blink_result(value, blinks) for value in stones)


def solve_part1(stones: Stones) -> int:
    return blink_total(stones, 25)


def solve_part2(stones: Stones) -> int:
    return blink_total(stones, 75)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 11.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    stones = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(stones)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(stones)}")


if __name__ == "__main__":
    main()
