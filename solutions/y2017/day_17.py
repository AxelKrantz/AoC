from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> int:
    return int(raw.strip())


def solve_part1(steps: int, insertions: int = 2017) -> int:
    buffer = [0]
    position = 0
    for value in range(1, insertions + 1):
        position = (position + steps) % len(buffer) + 1
        buffer.insert(position, value)
    return buffer[(position + 1) % len(buffer)]


def solve_part2(steps: int, insertions: int = 50_000_000) -> int:
    position = 0
    value_after_zero = 0
    length = 1
    for value in range(1, insertions + 1):
        position = (position + steps) % length + 1
        if position == 1:
            value_after_zero = value
        length += 1
    return value_after_zero


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 17.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--insertions1", type=int, default=2017)
    parser.add_argument("--insertions2", type=int, default=50_000_000)
    args = parser.parse_args()

    steps = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(steps, insertions=args.insertions1)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(steps, insertions=args.insertions2)}")


if __name__ == "__main__":
    main()
