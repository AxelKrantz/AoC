from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.strip().splitlines() if line.strip()]


def follow(instructions: Iterable[str], keypad: Sequence[Sequence[str]], start: tuple[int, int]) -> str:
    x, y = start
    code: list[str] = []
    height = len(keypad)
    width = len(keypad[0])
    for line in instructions:
        for move in line:
            if move == "U":
                nx, ny = x, max(0, y - 1)
            elif move == "D":
                nx, ny = x, min(height - 1, y + 1)
            elif move == "L":
                nx, ny = max(0, x - 1), y
            elif move == "R":
                nx, ny = min(width - 1, x + 1), y
            else:
                raise ValueError(f"Unknown move: {move}")
            if keypad[ny][nx] != " ":
                x, y = nx, ny
        code.append(keypad[y][x])
    return "".join(code)


SQUARE_KEYPAD = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
]

DIAMOND_KEYPAD = [
    [" ", " ", "1", " ", " "],
    [" ", "2", "3", "4", " "],
    ["5", "6", "7", "8", "9"],
    [" ", "A", "B", "C", " "],
    [" ", " ", "D", " ", " "],
]


def solve_part1(instructions: Iterable[str]) -> str:
    return follow(instructions, SQUARE_KEYPAD, start=(1, 1))


def solve_part2(instructions: Iterable[str]) -> str:
    return follow(instructions, DIAMOND_KEYPAD, start=(0, 2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 2.")
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
