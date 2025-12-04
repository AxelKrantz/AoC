from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence, Tuple


Point = tuple[int, int]


def parse(raw: str) -> list[Point]:
    points: list[Point] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))
    return points


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def bounding_box(points: Sequence[Point]) -> tuple[int, int, int, int]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def solve_part1(points: Sequence[Point]) -> int:
    min_x, max_x, min_y, max_y = bounding_box(points)
    area = [0] * len(points)
    infinite = set()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = [manhattan((x, y), point) for point in points]
            min_distance = min(distances)
            if distances.count(min_distance) > 1:
                continue
            idx = distances.index(min_distance)
            area[idx] += 1
            if x in (min_x, max_x) or y in (min_y, max_y):
                infinite.add(idx)

    return max(area[i] for i in range(len(points)) if i not in infinite)


def solve_part2(points: Sequence[Point], limit: int = 10000) -> int:
    min_x, max_x, min_y, max_y = bounding_box(points)
    safe_region = 0
    # expand search area by limit to ensure coverage
    padding = limit // len(points) + 1
    for x in range(min_x - padding, max_x + padding + 1):
        for y in range(min_y - padding, max_y + padding + 1):
            total_distance = sum(manhattan((x, y), point) for point in points)
            if total_distance < limit:
                safe_region += 1
    return safe_region


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 6.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    points = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(points)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(points)}")


if __name__ == "__main__":
    main()
