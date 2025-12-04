from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

Grid = list[list[str]]


def parse(raw: str) -> Grid:
    return [list(line.strip()) for line in raw.splitlines() if line.strip()]


NEIGHBORS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def count_adjacent(grid: Grid, row: int, col: int) -> int:
    height = len(grid)
    width = len(grid[0])
    count = 0
    for dr, dc in NEIGHBORS:
        r = row + dr
        c = col + dc
        if 0 <= r < height and 0 <= c < width and grid[r][c] == "@":
            count += 1
    return count


def solve_part1(grid: Grid) -> int:
    accessible = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != "@":
                continue
            if count_adjacent(grid, r, c) < 4:
                accessible += 1
    return accessible


def solve_part2(grid: Grid) -> int:
    height = len(grid)
    width = len(grid[0])
    removed = 0
    # Track current neighbor counts for "@"
    neighbor_counts = [[0] * width for _ in range(height)]
    for r in range(height):
        for c in range(width):
            if grid[r][c] == "@":
                neighbor_counts[r][c] = count_adjacent(grid, r, c)
    # Queue of accessible rolls
    from collections import deque

    q: deque[tuple[int, int]] = deque()
    for r in range(height):
        for c in range(width):
            if grid[r][c] == "@" and neighbor_counts[r][c] < 4:
                q.append((r, c))
    while q:
        r, c = q.popleft()
        if grid[r][c] != "@":
            continue
        grid[r][c] = "."
        removed += 1
        for dr, dc in NEIGHBORS:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == "@":
                neighbor_counts[nr][nc] -= 1
                if neighbor_counts[nr][nc] == 3:
                    q.append((nr, nc))
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 4.")
    parser.add_argument("input_path", type=Path, help="Path to puzzle input.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    grid = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(grid)}")
    if args.part in {"2", "both"}:
        # Use a fresh grid because part2 mutates
        grid_copy = [row.copy() for row in grid]
        print(f"Part 2: {solve_part2(grid_copy)}")


if __name__ == "__main__":
    main()
