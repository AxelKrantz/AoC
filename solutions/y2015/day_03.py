from __future__ import annotations

import argparse
from pathlib import Path

Vector = tuple[int, int]

MOVES: dict[str, Vector] = {
    "^": (0, 1),
    "v": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
}


def parse(raw: str) -> str:
    return raw.strip()


def walk(instructions: str, walkers: int = 1) -> int:
    positions = [(0, 0) for _ in range(walkers)]
    visited: set[Vector] = {(0, 0)}

    for index, move in enumerate(instructions):
        actor = index % walkers
        dx, dy = MOVES[move]
        x, y = positions[actor]
        positions[actor] = (x + dx, y + dy)
        visited.add(positions[actor])

    return len(visited)


def solve_part1(instructions: str) -> int:
    return walk(instructions, walkers=1)


def solve_part2(instructions: str) -> int:
    return walk(instructions, walkers=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 3.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    instructions = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(instructions)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(instructions)}")


if __name__ == "__main__":
    main()
