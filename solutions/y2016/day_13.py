from __future__ import annotations

import argparse
import collections
from pathlib import Path
from typing import Deque, Set, Tuple


def parse(raw: str) -> int:
    return int(raw.strip())


def is_open(x: int, y: int, puzzle_input: int) -> bool:
    if x < 0 or y < 0:
        return False
    n = x * x + 3 * x + 2 * x * y + y + y * y + puzzle_input
    return bin(n).count("1") % 2 == 0


def shortest_path(puzzle_input: int, target: tuple[int, int]) -> int:
    start = (1, 1)
    queue: Deque[tuple[int, int, int]] = collections.deque([(start[0], start[1], 0)])
    visited: Set[Tuple[int, int]] = {start}
    while queue:
        x, y, steps = queue.popleft()
        if (x, y) == target:
            return steps
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited:
                continue
            if not is_open(nx, ny, puzzle_input):
                continue
            visited.add((nx, ny))
            queue.append((nx, ny, steps + 1))
    raise ValueError("Target not reachable.")


def reachable_within(puzzle_input: int, distance: int) -> int:
    start = (1, 1)
    queue: Deque[tuple[int, int, int]] = collections.deque([(start[0], start[1], 0)])
    visited: Set[Tuple[int, int]] = {start}
    while queue:
        x, y, steps = queue.popleft()
        if steps == distance:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited:
                continue
            if not is_open(nx, ny, puzzle_input):
                continue
            visited.add((nx, ny))
            queue.append((nx, ny, steps + 1))
    return len(visited)


def solve_part1(puzzle_input: int, target: tuple[int, int] | None = None) -> int:
    goal = target or (31, 39)
    return shortest_path(puzzle_input, goal)


def solve_part2(puzzle_input: int, distance: int = 50) -> int:
    return reachable_within(puzzle_input, distance)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 13.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--target-x", type=int, default=31)
    parser.add_argument("--target-y", type=int, default=39)
    parser.add_argument("--distance", type=int, default=50)
    args = parser.parse_args()

    puzzle_input = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(puzzle_input, target=(args.target_x, args.target_y))}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(puzzle_input, distance=args.distance)}")


if __name__ == "__main__":
    main()
