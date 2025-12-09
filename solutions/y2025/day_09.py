from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

Point = tuple[int, int]


def parse(raw: str) -> list[Point]:
    points: list[Point] = []
    for line in raw.strip().splitlines():
        if not line.strip():
            continue
        x_str, y_str = line.split(",", 1)
        points.append((int(x_str), int(y_str)))
    return points


def rectangle_area(p1: Point, p2: Point) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def solve_part1(points: Sequence[Point]) -> int:
    best = 0
    for i, a in enumerate(points):
        for b in points[i + 1 :]:
            best = max(best, rectangle_area(a, b))
    return best


@dataclass(frozen=True)
class GridContext:
    outside_prefix: list[list[int]]
    x_to_idx: dict[int, int]
    y_to_idx: dict[int, int]


def build_grid(points: Sequence[Point]) -> GridContext:
    xs: set[int] = set()
    ys: set[int] = set()
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    for x, y in points:
        xs.add(x)
        xs.add(x + 1)
        ys.add(y)
        ys.add(y + 1)

    xs.update({min_x - 1, max_x + 2})
    ys.update({min_y - 1, max_y + 2})

    x_coords = sorted(xs)
    y_coords = sorted(ys)
    x_to_idx = {value: idx for idx, value in enumerate(x_coords)}
    y_to_idx = {value: idx for idx, value in enumerate(y_coords)}

    width = len(x_coords) - 1
    height = len(y_coords) - 1
    blocked = [bytearray(width) for _ in range(height)]

    pairs = list(zip(points, points[1:], strict=False))
    pairs.append((points[-1], points[0]))
    for (x1, y1), (x2, y2) in pairs:
        if x1 == x2:
            col = x_to_idx[x1]
            y_start, y_end = sorted((y1, y2))
            row_start = y_to_idx[y_start]
            row_end = y_to_idx[y_end + 1]
            for row in range(row_start, row_end):
                blocked[row][col] = 1
        elif y1 == y2:
            row = y_to_idx[y1]
            x_start, x_end = sorted((x1, x2))
            col_start = x_to_idx[x_start]
            col_end = x_to_idx[x_end + 1]
            for col in range(col_start, col_end):
                blocked[row][col] = 1
        else:
            raise ValueError("Input path must be axis-aligned between points.")

    outside = [bytearray(width) for _ in range(height)]
    queue: deque[tuple[int, int]] = deque()
    if not blocked[0][0]:
        outside[0][0] = 1
        queue.append((0, 0))

    while queue:
        row, col = queue.popleft()
        for d_row, d_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n_row = row + d_row
            n_col = col + d_col
            if 0 <= n_row < height and 0 <= n_col < width:
                if blocked[n_row][n_col] or outside[n_row][n_col]:
                    continue
                outside[n_row][n_col] = 1
                queue.append((n_row, n_col))

    outside_prefix: list[list[int]] = [[0] * (width + 1) for _ in range(height + 1)]
    for row in range(height):
        acc = 0
        for col in range(width):
            acc += outside[row][col]
            outside_prefix[row + 1][col + 1] = outside_prefix[row][col + 1] + acc

    return GridContext(outside_prefix=outside_prefix, x_to_idx=x_to_idx, y_to_idx=y_to_idx)


def rectangle_inside(context: GridContext, p1: Point, p2: Point) -> bool:
    x1, y1 = p1
    x2, y2 = p2
    x_low, x_high = sorted((x1, x2))
    y_low, y_high = sorted((y1, y2))

    col_start = context.x_to_idx[x_low]
    col_end = context.x_to_idx[x_high + 1]
    row_start = context.y_to_idx[y_low]
    row_end = context.y_to_idx[y_high + 1]

    prefix = context.outside_prefix
    outside_count = (
        prefix[row_end][col_end]
        - prefix[row_start][col_end]
        - prefix[row_end][col_start]
        + prefix[row_start][col_start]
    )
    return outside_count == 0


def solve_part2(points: Sequence[Point]) -> int:
    context = build_grid(points)
    best = 0
    for i, a in enumerate(points):
        for b in points[i + 1 :]:
            area = rectangle_area(a, b)
            if area <= best:
                continue
            if rectangle_inside(context, a, b):
                best = area
    return best


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 9.")
    parser.add_argument("input_path", type=Path, help="Path to puzzle input.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args(list(argv) if argv is not None else None)

    points = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(points)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(points)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
