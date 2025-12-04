from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple


GRID_SIZE = 300


def parse(raw: str) -> int:
    return int(raw.strip())


def power_level(x: int, y: int, serial: int) -> int:
    rack_id = x + 10
    power = (rack_id * y + serial) * rack_id
    digit = (power // 100) % 10
    return digit - 5


def build_prefix_sums(serial: int) -> list[list[int]]:
    prefix = [[0] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
    for y in range(1, GRID_SIZE + 1):
        row_total = 0
        for x in range(1, GRID_SIZE + 1):
            row_total += power_level(x, y, serial)
            prefix[y][x] = prefix[y - 1][x] + row_total
    return prefix


def square_sum(prefix: list[list[int]], x: int, y: int, size: int) -> int:
    x2 = x + size - 1
    y2 = y + size - 1
    return (
        prefix[y2][x2]
        - prefix[y - 1][x2]
        - prefix[y2][x - 1]
        + prefix[y - 1][x - 1]
    )


def solve_part1(serial: int) -> tuple[int, int]:
    prefix = build_prefix_sums(serial)
    best_power = float("-inf")
    best_coord = (0, 0)
    size = 3
    for y in range(1, GRID_SIZE - size + 2):
        for x in range(1, GRID_SIZE - size + 2):
            total = square_sum(prefix, x, y, size)
            if total > best_power:
                best_power = total
                best_coord = (x, y)
    return best_coord


def solve_part2(serial: int) -> tuple[int, int, int]:
    prefix = build_prefix_sums(serial)
    best_power = float("-inf")
    best = (0, 0, 0)
    for size in range(1, GRID_SIZE + 1):
        for y in range(1, GRID_SIZE - size + 2):
            for x in range(1, GRID_SIZE - size + 2):
                total = square_sum(prefix, x, y, size)
                if total > best_power:
                    best_power = total
                    best = (x, y, size)
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 11.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    serial = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        x, y = solve_part1(serial)
        print(f"Part 1: {x},{y}")
    if args.part in {"2", "both"}:
        x, y, size = solve_part2(serial)
        print(f"Part 2: {x},{y},{size}")


if __name__ == "__main__":
    main()

