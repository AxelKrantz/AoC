from __future__ import annotations

import argparse
from collections import defaultdict, deque
from pathlib import Path
from typing import DefaultDict, Iterable

Grid = list[list[str]]
Coordinate = tuple[int, int]


def parse(raw: str) -> Grid:
    return [list(line.strip()) for line in raw.splitlines() if line.strip()]


def neighbours(rows: int, cols: int, r: int, c: int) -> Iterable[Coordinate]:
    if r > 0:
        yield (r - 1, c)
    if r + 1 < rows:
        yield (r + 1, c)
    if c > 0:
        yield (r, c - 1)
    if c + 1 < cols:
        yield (r, c + 1)


def count_runs(values: Iterable[int]) -> int:
    sorted_values = sorted(values)
    if not sorted_values:
        return 0
    runs = 1
    for prev, current in zip(sorted_values, sorted_values[1:]):
        if current != prev + 1:
            runs += 1
    return runs


def explore_region(
    grid: Grid, start: Coordinate, visited: set[Coordinate]
) -> tuple[int, int, dict[str, DefaultDict[int, set[int]]]]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    target = grid[start[0]][start[1]]

    queue = deque([start])
    visited.add(start)

    area = 0
    perimeter = 0
    edges: dict[str, DefaultDict[int, set[int]]] = {
        "N": defaultdict(set),
        "S": defaultdict(set),
        "W": defaultdict(set),
        "E": defaultdict(set),
    }

    while queue:
        r, c = queue.popleft()
        area += 1

        # Check four sides of the current plot.
        # North
        if r == 0 or grid[r - 1][c] != target:
            perimeter += 1
            edges["N"][r].add(c)
        else:
            neighbour = (r - 1, c)
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
        # South
        if r + 1 == rows or grid[r + 1][c] != target:
            perimeter += 1
            edges["S"][r + 1].add(c)
        else:
            neighbour = (r + 1, c)
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
        # West
        if c == 0 or grid[r][c - 1] != target:
            perimeter += 1
            edges["W"][c].add(r)
        else:
            neighbour = (r, c - 1)
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
        # East
        if c + 1 == cols or grid[r][c + 1] != target:
            perimeter += 1
            edges["E"][c + 1].add(r)
        else:
            neighbour = (r, c + 1)
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return area, perimeter, edges


def region_sides(edges: dict[str, DefaultDict[int, set[int]]]) -> int:
    total_sides = 0
    for orientation in ("N", "S"):
        for row, columns in edges[orientation].items():
            total_sides += count_runs(columns)
    for orientation in ("W", "E"):
        for column, rows in edges[orientation].items():
            total_sides += count_runs(rows)
    return total_sides


def solve_part1(grid: Grid) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    visited: set[Coordinate] = set()
    total = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
            area, perimeter, _ = explore_region(grid, (r, c), visited)
            total += area * perimeter
    return total


def solve_part2(grid: Grid) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    visited: set[Coordinate] = set()
    total = 0

    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
            area, _, edges = explore_region(grid, (r, c), visited)
            sides = region_sides(edges)
            total += area * sides
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 12.")
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
