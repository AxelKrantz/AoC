from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Iterator, Tuple


def parse(raw: str) -> list[tuple[int, int, int]]:
    triangles: list[tuple[int, int, int]] = []
    for line in raw.strip().splitlines():
        if not line.strip():
            continue
        parts = [int(value) for value in line.split()]
        if len(parts) != 3:
            raise ValueError("Each line must contain exactly three side lengths.")
        triangles.append(tuple(parts))
    return triangles


def is_valid(triangle: tuple[int, int, int]) -> bool:
    a, b, c = sorted(triangle)
    return a + b > c


def solve_part1(triangles: Iterable[tuple[int, int, int]]) -> int:
    return sum(1 for triangle in triangles if is_valid(triangle))


def vertical_groups(triangles: list[tuple[int, int, int]]) -> Iterator[tuple[int, int, int]]:
    for i in range(0, len(triangles), 3):
        chunk = triangles[i : i + 3]
        if len(chunk) < 3:
            continue
        for column in range(3):
            yield chunk[0][column], chunk[1][column], chunk[2][column]


def solve_part2(triangles: list[tuple[int, int, int]]) -> int:
    return sum(1 for triangle in vertical_groups(triangles) if is_valid(triangle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 3.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    triangles = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(triangles)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(triangles)}")


if __name__ == "__main__":
    main()
