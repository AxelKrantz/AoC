from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple


def parse(raw: str) -> List[str]:
    return [line.rstrip("\n") for line in raw.splitlines()]


DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def traverse(diagram: List[str]) -> Tuple[str, int]:
    width = max(len(row) for row in diagram)
    height = len(diagram)

    def char_at(x: int, y: int) -> str:
        if 0 <= y < height and 0 <= x < len(diagram[y]):
            return diagram[y][x]
        return " "

    x = diagram[0].index("|")
    y = 0
    direction = "down"
    letters: list[str] = []
    steps = 0

    while True:
        char = char_at(x, y)
        if char == " ":
            break
        steps += 1
        if char.isalpha():
            letters.append(char)
        if char == "+":
            if direction in {"up", "down"}:
                if char_at(x - 1, y) != " ":
                    direction = "left"
                elif char_at(x + 1, y) != " ":
                    direction = "right"
            else:
                if char_at(x, y - 1) != " ":
                    direction = "up"
                elif char_at(x, y + 1) != " ":
                    direction = "down"
        dx, dy = DIRECTIONS[direction]
        x += dx
        y += dy
    return "".join(letters), steps


def solve_part1(diagram: List[str]) -> str:
    letters, _ = traverse(diagram)
    return letters


def solve_part2(diagram: List[str]) -> int:
    _, steps = traverse(diagram)
    return steps


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 19.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    diagram = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(diagram)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(diagram)}")


if __name__ == "__main__":
    main()
