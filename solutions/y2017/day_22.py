from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Set, Tuple


Grid = Dict[Tuple[int, int], int]


def parse(raw: str) -> Grid:
    grid: Grid = {}
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    offset = len(lines) // 2
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                grid[(x - offset, y - offset)] = 2  # infected state
    return grid


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def solve_part1(grid: Grid, bursts: int = 10_000) -> int:
    infected: Set[Tuple[int, int]] = {pos for pos, state in grid.items() if state == 2}
    x = y = 0
    direction_index = 0
    infections = 0
    for _ in range(bursts):
        if (x, y) in infected:
            direction_index = (direction_index + 1) % 4
            infected.remove((x, y))
        else:
            direction_index = (direction_index - 1) % 4
            infected.add((x, y))
            infections += 1
        dx, dy = DIRECTIONS[direction_index]
        x += dx
        y += dy
    return infections


def solve_part2(grid: Grid, bursts: int = 10_000_000) -> int:
    states = grid.copy()  # 0: clean, 1: weakened, 2: infected, 3: flagged
    x = y = 0
    direction_index = 0
    infections = 0
    for _ in range(bursts):
        state = states.get((x, y), 0)
        if state == 0:  # clean
            direction_index = (direction_index - 1) % 4
            states[(x, y)] = 1
        elif state == 1:  # weakened
            states[(x, y)] = 2
            infections += 1
        elif state == 2:  # infected
            direction_index = (direction_index + 1) % 4
            states[(x, y)] = 3
        elif state == 3:  # flagged
            direction_index = (direction_index + 2) % 4
            states[(x, y)] = 0
        dx, dy = DIRECTIONS[direction_index]
        x += dx
        y += dy
    return infections


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 22.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--bursts1", type=int, default=10_000)
    parser.add_argument("--bursts2", type=int, default=10_000_000)
    args = parser.parse_args()

    grid = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(grid, bursts=args.bursts1)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(grid, bursts=args.bursts2)}")


if __name__ == "__main__":
    main()
