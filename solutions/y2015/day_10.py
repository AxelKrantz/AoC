from __future__ import annotations

import argparse
from itertools import groupby
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def look_and_say(sequence: str) -> str:
    parts: list[str] = []
    for digit, group in groupby(sequence):
        count = sum(1 for _ in group)
        parts.append(f"{count}{digit}")
    return "".join(parts)


def iterate(sequence: str, times: int) -> str:
    current = sequence
    for _ in range(times):
        current = look_and_say(current)
    return current


def solve_part1(sequence: str) -> int:
    return len(iterate(sequence, 40))


def solve_part2(sequence: str) -> int:
    return len(iterate(sequence, 50))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 10.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    sequence = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(sequence)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(sequence)}")


if __name__ == "__main__":
    main()
