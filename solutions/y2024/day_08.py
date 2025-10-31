from __future__ import annotations

import argparse
from collections import defaultdict
from math import gcd
from pathlib import Path
from typing import Iterable, Sequence

Grid = list[str]
Coordinate = tuple[int, int]


def parse(raw: str) -> tuple[Grid, dict[str, list[Coordinate]]]:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    frequencies: dict[str, list[Coordinate]] = defaultdict(list)
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch != ".":
                frequencies[ch].append((r, c))
    return lines, frequencies


def in_bounds(rows: int, cols: int, position: Coordinate) -> bool:
    r, c = position
    return 0 <= r < rows and 0 <= c < cols


def part1_antinodes(rows: int, cols: int, groups: dict[str, list[Coordinate]]) -> set[Coordinate]:
    antinodes: set[Coordinate] = set()
    for positions in groups.values():
        count = len(positions)
        if count < 2:
            continue
        for i in range(count):
            r1, c1 = positions[i]
            for j in range(i + 1, count):
                r2, c2 = positions[j]
                dr = r2 - r1
                dc = c2 - c1
                candidates = [
                    (r1 - dr, c1 - dc),
                    (r2 + dr, c2 + dc),
                ]
                for candidate in candidates:
                    if in_bounds(rows, cols, candidate):
                        antinodes.add(candidate)
    return antinodes


def normalized_step(dr: int, dc: int) -> Coordinate:
    factor = gcd(abs(dr), abs(dc))
    if factor == 0:
        return (0, 0)
    return (dr // factor, dc // factor)


def part2_antinodes(rows: int, cols: int, groups: dict[str, list[Coordinate]]) -> set[Coordinate]:
    antinodes: set[Coordinate] = set()
    for positions in groups.values():
        count = len(positions)
        if count < 2:
            continue
        for i in range(count):
            r1, c1 = positions[i]
            for j in range(i + 1, count):
                r2, c2 = positions[j]
                step_r, step_c = normalized_step(r2 - r1, c2 - c1)
                if step_r == 0 and step_c == 0:
                    continue

                # Find the furthest reachable point in the negative direction.
                start_r, start_c = r1, c1
                while True:
                    next_r = start_r - step_r
                    next_c = start_c - step_c
                    if not in_bounds(rows, cols, (next_r, next_c)):
                        break
                    start_r, start_c = next_r, next_c

                # Walk forward across the grid, collecting all positions along the line.
                cur_r, cur_c = start_r, start_c
                while in_bounds(rows, cols, (cur_r, cur_c)):
                    antinodes.add((cur_r, cur_c))
                    cur_r += step_r
                    cur_c += step_c
    return antinodes


def solve_part1(grid: Grid, groups: dict[str, list[Coordinate]]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return len(part1_antinodes(rows, cols, groups))


def solve_part2(grid: Grid, groups: dict[str, list[Coordinate]]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return len(part2_antinodes(rows, cols, groups))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 8.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    grid, groups = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(grid, groups)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(grid, groups)}")


if __name__ == "__main__":
    main()
