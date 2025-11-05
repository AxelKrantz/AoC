from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Instruction:
    turn: str
    steps: int


def parse(raw: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for item in raw.strip().split(","):
        token = item.strip()
        if not token:
            continue
        instructions.append(Instruction(token[0], int(token[1:])))
    return instructions


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def follow(instructions: Iterable[Instruction]) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    x = y = 0
    direction_index = 0
    path: list[tuple[int, int]] = [(x, y)]
    for instruction in instructions:
        if instruction.turn == "R":
            direction_index = (direction_index + 1) % 4
        elif instruction.turn == "L":
            direction_index = (direction_index - 1) % 4
        else:
            raise ValueError(f"Unknown turn: {instruction.turn}")
        dx, dy = DIRECTIONS[direction_index]
        for _ in range(instruction.steps):
            x += dx
            y += dy
            path.append((x, y))
    return (x, y), path


def manhattan(position: tuple[int, int]) -> int:
    x, y = position
    return abs(x) + abs(y)


def solve_part1(instructions: Iterable[Instruction]) -> int:
    final_position, _ = follow(instructions)
    return manhattan(final_position)


def solve_part2(instructions: Iterable[Instruction]) -> int:
    _, path = follow(instructions)
    seen: set[tuple[int, int]] = set()
    for position in path:
        if position in seen:
            return manhattan(position)
        seen.add(position)
    raise ValueError("No location visited twice.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 1.")
    parser.add_argument("input_path", type=Path)
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
