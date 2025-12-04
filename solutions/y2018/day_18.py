from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, Iterator, Sequence, Tuple

Grid = tuple[str, ...]


def parse(raw: str) -> Grid:
    return tuple(line.strip() for line in raw.strip().splitlines() if line.strip())


def neighbors(x: int, y: int, width: int, height: int) -> Iterator[Tuple[int, int]]:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < width and 0 <= ny < height:
                yield nx, ny


def step(area: Grid) -> Grid:
    height = len(area)
    width = len(area[0]) if height else 0
    new_rows: list[str] = []
    for y in range(height):
        row_chars: list[str] = []
        for x in range(width):
            acre = area[y][x]
            woods = 0
            yards = 0
            for nx, ny in neighbors(x, y, width, height):
                neighbor = area[ny][nx]
                if neighbor == "|":
                    woods += 1
                elif neighbor == "#":
                    yards += 1
            if acre == ".":
                row_chars.append("|" if woods >= 3 else ".")
            elif acre == "|":
                row_chars.append("#" if yards >= 3 else "|")
            else:  # '#'
                row_chars.append("#" if yards >= 1 and woods >= 1 else ".")
        new_rows.append("".join(row_chars))
    return tuple(new_rows)


def resource_value(area: Grid) -> int:
    wooded = sum(row.count("|") for row in area)
    lumberyards = sum(row.count("#") for row in area)
    return wooded * lumberyards


def simulate(area: Grid, minutes: int) -> Grid:
    seen: Dict[Grid, int] = {}
    history: list[Grid] = []
    for minute in range(minutes):
        if area in seen:
            cycle_start = seen[area]
            cycle_length = minute - cycle_start
            remaining = (minutes - minute) % cycle_length
            return history[cycle_start + remaining]
        seen[area] = minute
        history.append(area)
        area = step(area)
    return area


def solve_part1(area: Grid) -> int:
    final_area = area
    for _ in range(10):
        final_area = step(final_area)
    return resource_value(final_area)


def solve_part2(area: Grid) -> int:
    final_area = simulate(area, 1_000_000_000)
    return resource_value(final_area)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 18.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    data = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
