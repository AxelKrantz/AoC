from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple


def parse(raw: str) -> list[str]:
    return [step for step in raw.strip().split(",") if step]


DIRECTIONS = {
    "n": (0, 1, -1),
    "ne": (1, 0, -1),
    "se": (1, -1, 0),
    "s": (0, -1, 1),
    "sw": (-1, 0, 1),
    "nw": (-1, 1, 0),
}


def add(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def distance(position: Tuple[int, int, int]) -> int:
    return max(abs(position[0]), abs(position[1]), abs(position[2]))


def walk(steps: Iterable[str]) -> tuple[int, int]:
    pos = (0, 0, 0)
    max_distance = 0
    for step in steps:
        pos = add(pos, DIRECTIONS[step])
        max_distance = max(max_distance, distance(pos))
    return distance(pos), max_distance


def solve_part1(steps: list[str]) -> int:
    final, _ = walk(steps)
    return final


def solve_part2(steps: list[str]) -> int:
    _, furthest = walk(steps)
    return furthest


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 11.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    steps = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(steps)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(steps)}")


if __name__ == "__main__":
    main()
