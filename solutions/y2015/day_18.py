from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Set, Tuple

Point = tuple[int, int]


def parse(raw: str) -> tuple[Set[Point], int, int]:
    lines = [line.strip() for line in raw.strip().splitlines() if line]
    lights: set[Point] = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                lights.add((x, y))
    width = len(lines[0])
    height = len(lines)
    return lights, width, height


def neighbors(point: Point) -> Iterable[Point]:
    x, y = point
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            yield x + dx, y + dy


def step(
    lights: Set[Point], width: int, height: int, *, stuck_corners: bool
) -> Set[Point]:
    corners = {(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)}
    next_state: set[Point] = set()
    for y in range(height):
        for x in range(width):
            point = (x, y)
            active_neighbors = sum(
                (nx, ny) in lights
                for nx, ny in neighbors(point)
                if 0 <= nx < width and 0 <= ny < height
            )
            if point in lights and active_neighbors in (2, 3):
                next_state.add(point)
            if point not in lights and active_neighbors == 3:
                next_state.add(point)
    if stuck_corners:
        next_state.update(corners)
    return next_state


def animate(
    lights: Set[Point],
    width: int,
    height: int,
    steps: int,
    *,
    stuck_corners: bool = False,
) -> Set[Point]:
    current = set(lights)
    corners = {(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)}
    if stuck_corners:
        current.update(corners)
    for _ in range(steps):
        current = step(current, width, height, stuck_corners=stuck_corners)
    return current


def solve_part1(data: tuple[Set[Point], int, int], steps: int = 100) -> int:
    lights, width, height = data
    return len(animate(lights, width, height, steps))


def solve_part2(data: tuple[Set[Point], int, int], steps: int = 100) -> int:
    lights, width, height = data
    return len(animate(lights, width, height, steps, stuck_corners=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 18.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--steps", type=int, default=100)
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    data = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data, steps=args.steps)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data, steps=args.steps)}")


if __name__ == "__main__":
    main()
