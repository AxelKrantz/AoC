from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Tuple

Instruction = Tuple[str, int, int, int, int]


def parse(raw: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in raw.splitlines():
        if not line:
            continue
        if line.startswith("turn on"):
            action = "on"
            rest = line[len("turn on ") :]
        elif line.startswith("turn off"):
            action = "off"
            rest = line[len("turn off ") :]
        elif line.startswith("toggle"):
            action = "toggle"
            rest = line[len("toggle ") :]
        else:
            raise ValueError(f"Unrecognized instruction: {line}")

        coords, _, end = rest.partition(" through ")
        x1_str, _, y1_str = coords.partition(",")
        x2_str, _, y2_str = end.partition(",")
        instructions.append((action, int(x1_str), int(y1_str), int(x2_str), int(y2_str)))
    return instructions


def solve_part1(instructions: Iterable[Instruction]) -> int:
    grid = [[False] * 1000 for _ in range(1000)]
    for action, x1, y1, x2, y2 in instructions:
        for x in range(x1, x2 + 1):
            row = grid[x]
            if action == "on":
                for y in range(y1, y2 + 1):
                    row[y] = True
            elif action == "off":
                for y in range(y1, y2 + 1):
                    row[y] = False
            else:  # toggle
                for y in range(y1, y2 + 1):
                    row[y] = not row[y]
    return sum(sum(1 for cell in row if cell) for row in grid)


def solve_part2(instructions: Iterable[Instruction]) -> int:
    grid = [[0] * 1000 for _ in range(1000)]
    for action, x1, y1, x2, y2 in instructions:
        for x in range(x1, x2 + 1):
            row = grid[x]
            if action == "on":
                for y in range(y1, y2 + 1):
                    row[y] += 1
            elif action == "off":
                for y in range(y1, y2 + 1):
                    if row[y] > 0:
                        row[y] -= 1
            else:  # toggle
                for y in range(y1, y2 + 1):
                    row[y] += 2
    return sum(sum(row) for row in grid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 6.")
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
