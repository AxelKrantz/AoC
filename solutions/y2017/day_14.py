from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Iterable, Set, Tuple

from solutions.y2017 import day_10


def parse(raw: str) -> str:
    return raw.strip()


def row_bits(key: str, index: int) -> str:
    hash_hex = day_10.knot_hash(f"{key}-{index}")
    return "".join(f"{int(char, 16):04b}" for char in hash_hex)


def generate_grid(key: str) -> Iterable[str]:
    for row in range(128):
        yield row_bits(key, row)


def solve_part1(key: str) -> int:
    return sum(row.count("1") for row in generate_grid(key))


def count_regions(key: str) -> int:
    grid = list(generate_grid(key))
    visited: Set[Tuple[int, int]] = set()
    regions = 0
    for y in range(128):
        for x in range(128):
            if grid[y][x] == "0" or (x, y) in visited:
                continue
            regions += 1
            queue = deque([(x, y)])
            while queue:
                cx, cy = queue.popleft()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < 128 and 0 <= ny < 128 and grid[ny][nx] == "1" and (nx, ny) not in visited:
                        queue.append((nx, ny))
    return regions


def solve_part2(key: str) -> int:
    return count_regions(key)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 14.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    key = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(key)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(key)}")


if __name__ == "__main__":
    main()
