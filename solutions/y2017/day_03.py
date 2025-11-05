from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple


def parse(raw: str) -> int:
    return int(raw.strip())


def spiral_distance(target: int) -> int:
    if target == 1:
        return 0
    layer = 0
    while (2 * layer + 1) ** 2 < target:
        layer += 1
    side_len = 2 * layer
    max_value = (2 * layer + 1) ** 2
    steps_from_corner = (max_value - target) % side_len
    return layer + abs(steps_from_corner - layer)


def spiral_sum(target: int) -> int:
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    values: Dict[Tuple[int, int], int] = defaultdict(int)
    x = y = 0
    values[(0, 0)] = 1
    step_length = 1
    direction_index = 0

    def neighbors_sum(px: int, py: int) -> int:
        total = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                total += values[(px + dx, py + dy)]
        return total

    while True:
        for _ in range(2):
            dx, dy = directions[direction_index % 4]
            for _ in range(step_length):
                x += dx
                y += dy
                val = neighbors_sum(x, y)
                values[(x, y)] = val
                if val > target:
                    return val
            direction_index += 1
        step_length += 1


def solve_part1(target: int) -> int:
    return spiral_distance(target)


def solve_part2(target: int) -> int:
    return spiral_sum(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 3.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    target = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(target)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(target)}")


if __name__ == "__main__":
    main()
