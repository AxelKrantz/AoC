from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

Grid = list[list[str]]


def parse(raw: str) -> Grid:
    return [list(line.strip()) for line in raw.splitlines() if line.strip()]


DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def solve_part1(grid: Grid) -> int:
    target = "XMAS"
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    total = 0
    for r in range(rows):
        for c in range(cols):
            for dr, dc in DIRECTIONS:
                rr, cc = r, c
                match = True
                for ch in target:
                    if not (0 <= rr < rows and 0 <= cc < cols and grid[rr][cc] == ch):
                        match = False
                        break
                    rr += dr
                    cc += dc
                if match:
                    total += 1
    return total


def solve_part2(grid: Grid) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    total = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != "A":
                continue
            diag1 = grid[r - 1][c - 1] + grid[r + 1][c + 1]
            diag2 = grid[r - 1][c + 1] + grid[r + 1][c - 1]
            if diag1 in {"MS", "SM"} and diag2 in {"MS", "SM"}:
                total += 1
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 4.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    grid = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(grid)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(grid)}")


if __name__ == "__main__":
    main()
