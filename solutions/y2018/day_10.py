from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

POINT_PATTERN = re.compile(
    r"position=<\s*(?P<x>-?\d+),\s*(?P<y>-?\d+)> velocity=<\s*(?P<vx>-?\d+),\s*(?P<vy>-?\d+)>"
)


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    vx: int
    vy: int


def parse(raw: str) -> list[Point]:
    points: list[Point] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = POINT_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"Unable to parse point: {line!r}")
        points.append(
            Point(
                x=int(match.group("x")),
                y=int(match.group("y")),
                vx=int(match.group("vx")),
                vy=int(match.group("vy")),
            )
        )
    return points


def advance(points: Sequence[Point], seconds: int) -> list[tuple[int, int]]:
    return [(p.x + p.vx * seconds, p.y + p.vy * seconds) for p in points]


def bounding_box(coords: Iterable[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs, ys = zip(*coords)
    return min(xs), max(xs), min(ys), max(ys)


def render(points: Sequence[tuple[int, int]]) -> list[str]:
    min_x, max_x, min_y, max_y = bounding_box(points)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = [["."] * width for _ in range(height)]
    for x, y in points:
        grid[y - min_y][x - min_x] = "#"
    return ["".join(row) for row in grid]


def find_alignment(points: Sequence[Point]) -> tuple[list[str], int]:
    best_time = 0
    best_area = math.inf
    best_positions: list[tuple[int, int]] = advance(points, 0)

    time = 0
    while True:
        positions = advance(points, time)
        min_x, max_x, min_y, max_y = bounding_box(positions)
        area = (max_x - min_x) * (max_y - min_y)
        if area < best_area:
            best_area = area
            best_time = time
            best_positions = positions
        else:
            if area > best_area:
                break
        time += 1
    return render(best_positions), best_time


def solve_part1(points: Sequence[Point]) -> str:
    message, _ = find_alignment(points)
    return "\n".join(message)


def solve_part2(points: Sequence[Point]) -> int:
    _, seconds = find_alignment(points)
    return seconds


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 10.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    points = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print("Part 1:")
        print(solve_part1(points))
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(points)}")


if __name__ == "__main__":
    main()

