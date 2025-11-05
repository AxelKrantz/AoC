from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict


def parse(raw: str) -> Dict[int, int]:
    layers: dict[int, int] = {}
    for line in raw.strip().splitlines():
        if not line.strip():
            continue
        depth_str, range_str = line.split(":")
        layers[int(depth_str.strip())] = int(range_str.strip())
    return layers


def severity(layers: Dict[int, int], delay: int = 0) -> int:
    total = 0
    for depth, scanner_range in layers.items():
        period = 2 * (scanner_range - 1)
        if (depth + delay) % period == 0:
            total += depth * scanner_range
    return total


def is_safe(layers: Dict[int, int], delay: int) -> bool:
    for depth, scanner_range in layers.items():
        period = 2 * (scanner_range - 1)
        if (depth + delay) % period == 0:
            return False
    return True


def solve_part1(layers: Dict[int, int]) -> int:
    return severity(layers)


def solve_part2(layers: Dict[int, int]) -> int:
    delay = 0
    while not is_safe(layers, delay):
        delay += 1
    return delay


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 13.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    layers = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(layers)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(layers)}")


if __name__ == "__main__":
    main()
