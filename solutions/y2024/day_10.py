from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
from typing import Iterable

Grid = list[list[int]]
Coordinate = tuple[int, int]


def parse(raw: str) -> Grid:
    return [list(map(int, line.strip())) for line in raw.splitlines() if line.strip()]


def neighbours(rows: int, cols: int, r: int, c: int) -> Iterable[Coordinate]:
    if r > 0:
        yield (r - 1, c)
    if r + 1 < rows:
        yield (r + 1, c)
    if c > 0:
        yield (r, c - 1)
    if c + 1 < cols:
        yield (r, c + 1)


def solve_part1(grid: Grid) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def trailhead_score(r: int, c: int) -> int:
        reachable: set[Coordinate] = set()
        visited: set[Coordinate] = set()

        def dfs(rr: int, cc: int) -> None:
            if (rr, cc) in visited:
                return
            visited.add((rr, cc))
            height = grid[rr][cc]
            if height == 9:
                reachable.add((rr, cc))
                return
            for nr, nc in neighbours(rows, cols, rr, cc):
                if grid[nr][nc] == height + 1:
                    dfs(nr, nc)

        dfs(r, c)
        return len(reachable)

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total += trailhead_score(r, c)
    return total


def solve_part2(grid: Grid) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    @lru_cache(maxsize=None)
    def count_paths(r: int, c: int) -> int:
        height = grid[r][c]
        if height == 9:
            return 1
        total_paths = 0
        for nr, nc in neighbours(rows, cols, r, c):
            if grid[nr][nc] == height + 1:
                total_paths += count_paths(nr, nc)
        return total_paths

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total += count_paths(r, c)
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 10.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    grid = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(grid)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(grid)}")


if __name__ == "__main__":
    main()
