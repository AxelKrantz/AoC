from __future__ import annotations

import argparse
import collections
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

Grid = List[str]
Point = Tuple[int, int]


def parse(raw: str) -> tuple[Grid, Dict[str, Point]]:
    grid = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    locations: dict[str, Point] = {}
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch.isdigit():
                locations[ch] = (x, y)
    return grid, locations


def neighbours(point: Point) -> Iterable[Point]:
    x, y = point
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yield x + dx, y + dy


def bfs(grid: Grid, start: Point) -> Dict[Point, int]:
    width = len(grid[0])
    height = len(grid)
    queue = collections.deque([(start, 0)])
    distances: dict[Point, int] = {start: 0}
    while queue:
        point, dist = queue.popleft()
        for nx, ny in neighbours(point):
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if grid[ny][nx] == "#":
                continue
            if (nx, ny) in distances:
                continue
            distances[(nx, ny)] = dist + 1
            queue.append(((nx, ny), dist + 1))
    return distances


def pairwise_distances(grid: Grid, locations: Dict[str, Point]) -> Dict[tuple[str, str], int]:
    distances: dict[tuple[str, str], int] = {}
    for label, position in locations.items():
        dists = bfs(grid, position)
        for other_label, other_position in locations.items():
            if label == other_label:
                continue
            distances[(label, other_label)] = dists[other_position]
    return distances


def shortest_path(distances: Dict[tuple[str, str], int], points: List[str], return_to_start: bool) -> int:
    start = "0"
    others = [p for p in points if p != start]

    @lru_cache(maxsize=None)
    def dp(current: str, remaining: tuple[str, ...]) -> int:
        if not remaining:
            return distances[(current, start)] if return_to_start else 0
        best = float("inf")
        for index, nxt in enumerate(remaining):
            rest = remaining[:index] + remaining[index + 1 :]
            cost = distances[(current, nxt)] + dp(nxt, rest)
            best = min(best, cost)
        return int(best)

    return dp(start, tuple(sorted(others)))


def solve_part1(parsed: tuple[Grid, Dict[str, Point]]) -> int:
    grid, locations = parsed
    distances = pairwise_distances(grid, locations)
    return shortest_path(distances, sorted(locations.keys()), return_to_start=False)


def solve_part2(parsed: tuple[Grid, Dict[str, Point]]) -> int:
    grid, locations = parsed
    distances = pairwise_distances(grid, locations)
    return shortest_path(distances, sorted(locations.keys()), return_to_start=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 24.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    parsed = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(parsed)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(parsed)}")


if __name__ == "__main__":
    main()
