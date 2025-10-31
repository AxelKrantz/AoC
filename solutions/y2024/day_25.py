from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

Shape = tuple[str, ...]
Heights = tuple[int, ...]


def parse(raw: str) -> tuple[list[Shape], list[Shape]]:
    locks: list[Shape] = []
    keys: list[Shape] = []
    blocks = raw.strip().split("\n\n")
    for block in blocks:
        rows = tuple(block.splitlines())
        if not rows:
            continue
        if rows[0].startswith("#"):
            locks.append(rows)
        else:
            keys.append(rows)
    return locks, keys


def to_heights(shape: Shape) -> Heights:
    rows = len(shape)
    cols = len(shape[0])
    heights: list[int] = [0] * cols
    for col in range(cols):
        count = sum(1 for row in range(rows) if shape[row][col] == "#")
        heights[col] = count - 1  # remove the always-filled base row
    return tuple(heights)


def fits(lock: Heights, key: Heights, interior_height: int) -> bool:
    return all(l + k <= interior_height for l, k in zip(lock, key))


def solve_part1(raw: str) -> int:
    locks_raw, keys_raw = parse(raw)
    if not locks_raw or not keys_raw:
        return 0
    interior_height = len(locks_raw[0]) - 2
    locks = [to_heights(shape) for shape in locks_raw]
    keys = [to_heights(shape) for shape in keys_raw]
    total = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key, interior_height):
                total += 1
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 25.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    print(solve_part1(raw))


if __name__ == "__main__":
    main()
