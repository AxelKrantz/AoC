from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> int:
    return int(raw.strip())


def josephus_last(n: int) -> int:
    highest_power = 1 << (n.bit_length() - 1)
    return 2 * (n - highest_power) + 1


def solve_part1(elves: int) -> int:
    return josephus_last(elves)


def solve_part2(elves: int) -> int:
    power = 1
    while power * 3 <= elves:
        power *= 3
    if elves == power:
        return elves
    return elves - power + max(elves - 2 * power, 0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 19.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    elves = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(elves)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(elves)}")


if __name__ == "__main__":
    main()
