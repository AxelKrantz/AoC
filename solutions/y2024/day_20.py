from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Grid = list[str]
Coordinate = tuple[int, int]


def parse(raw: str) -> Grid:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def find_char(grid: Grid, target: str) -> Coordinate:
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == target:
                return x, y
    raise ValueError(f"Character {target!r} not found.")


def in_bounds(grid: Grid, x: int, y: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def neighbors(grid: Grid, x: int, y: int) -> Iterable[Coordinate]:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if in_bounds(grid, nx, ny) and grid[ny][nx] != "#":
            yield nx, ny


def bfs_distances(grid: Grid, start: Coordinate) -> Dict[Coordinate, int]:
    queue: deque[tuple[Coordinate, int]] = deque([(start, 0)])
    distances: Dict[Coordinate, int] = {start: 0}
    while queue:
        (x, y), steps = queue.popleft()
        for nx, ny in neighbors(grid, x, y):
            if (nx, ny) not in distances:
                distances[(nx, ny)] = steps + 1
                queue.append(((nx, ny), steps + 1))
    return distances


def count_cheats(
    grid: Grid, cheat_limit: int, min_savings: int
) -> int:
    start = find_char(grid, "S")
    end = find_char(grid, "E")

    dist_from_start = bfs_distances(grid, start)
    dist_to_end = bfs_distances(grid, end)

    baseline = dist_from_start[end]

    track_cells = [
        (x, y)
        for y, row in enumerate(grid)
        for x, ch in enumerate(row)
        if ch != "#"
    ]

    total = 0
    for ax, ay in track_cells:
        start_dist = dist_from_start.get((ax, ay))
        if start_dist is None:
            continue
        for dx in range(-cheat_limit, cheat_limit + 1):
            remaining = cheat_limit - abs(dx)
            for dy in range(-remaining, remaining + 1):
                bx, by = ax + dx, ay + dy
                if (bx, by) == (ax, ay):
                    continue
                if not in_bounds(grid, bx, by):
                    continue
                if grid[by][bx] == "#":
                    continue
                end_dist = dist_to_end.get((bx, by))
                if end_dist is None:
                    continue
                cheat_length = abs(dx) + abs(dy)
                total_time = start_dist + cheat_length + end_dist
                saving = baseline - total_time
                if saving >= min_savings:
                    total += 1
    return total


def solve_part1(grid: Grid) -> int:
    return count_cheats(grid, cheat_limit=2, min_savings=100)


def solve_part2(grid: Grid) -> int:
    return count_cheats(grid, cheat_limit=20, min_savings=100)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 20.")
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
