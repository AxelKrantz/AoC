from __future__ import annotations

import argparse
from itertools import cycle
from pathlib import Path
from typing import Iterable, Sequence


def parse(raw: str) -> list[int]:
    return [int(line) for line in raw.strip().splitlines() if line]


def solve_part1(changes: Iterable[int]) -> int:
    return sum(changes)


def solve_part2(changes: Sequence[int]) -> int:
    seen = {0}
    frequency = 0

    for delta in cycle(changes):
        frequency += delta
        if frequency in seen:
            return frequency
        seen.add(frequency)

    raise RuntimeError("No repeated frequency found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 1.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    changes = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(changes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(changes)}")


if __name__ == "__main__":
    main()

