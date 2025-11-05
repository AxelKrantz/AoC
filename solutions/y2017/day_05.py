from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> list[int]:
    return [int(line) for line in raw.strip().splitlines() if line.strip()]


def steps_to_exit(offsets: list[int], strange: bool = False) -> int:
    instructions = offsets[:]
    position = 0
    steps = 0
    while 0 <= position < len(instructions):
        jump = instructions[position]
        if strange and jump >= 3:
            instructions[position] -= 1
        else:
            instructions[position] += 1
        position += jump
        steps += 1
    return steps


def solve_part1(offsets: list[int]) -> int:
    return steps_to_exit(offsets, strange=False)


def solve_part2(offsets: list[int]) -> int:
    return steps_to_exit(offsets, strange=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 5.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    offsets = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(offsets)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(offsets)}")


if __name__ == "__main__":
    main()
