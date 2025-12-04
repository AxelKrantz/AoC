from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Sequence, Set, Tuple

sys.setrecursionlimit(20000)

Coordinate = tuple[int, int]


@dataclass(frozen=True)
class Reservoir:
    clay: frozenset[Coordinate]
    min_y: int
    max_y: int


def parse(raw: str) -> Reservoir:
    clay: set[Coordinate] = set()
    for line in raw.strip().splitlines():
        left, right = line.split(", ")
        if left.startswith("x="):
            x = int(left.split("=")[1])
            y_start, y_end = (int(value) for value in right[2:].split(".."))
            for y in range(y_start, y_end + 1):
                clay.add((x, y))
        else:
            y = int(left.split("=")[1])
            x_start, x_end = (int(value) for value in right[2:].split(".."))
            for x in range(x_start, x_end + 1):
                clay.add((x, y))
    min_y = min(y for _x, y in clay)
    max_y = max(y for _x, y in clay)
    return Reservoir(clay=frozenset(clay), min_y=min_y, max_y=max_y)


def simulate(reservoir: Reservoir) -> tuple[Set[Coordinate], Set[Coordinate]]:
    clay = set(reservoir.clay)
    min_y = reservoir.min_y
    max_y = reservoir.max_y
    flowing: set[Coordinate] = set()
    settled: set[Coordinate] = set()

    def is_blocked(pos: Coordinate) -> bool:
        return pos in clay or pos in settled

    def flow(x: int, y: int) -> None:
        if y > max_y:
            return
        pos = (x, y)
        if pos in clay or pos in settled or pos in flowing:
            return
        flowing.add(pos)

        below = (x, y + 1)
        if not is_blocked(below):
            flow(x, y + 1)
        if not is_blocked(below):
            return

        left_blocked, left_cells = spread(x, y, -1)
        right_blocked, right_cells = spread(x, y, 1)

        if left_blocked and right_blocked:
            settled.add(pos)
            for cell in left_cells + right_cells:
                settled.add(cell)

    def spread(x: int, y: int, direction: int) -> tuple[bool, List[Coordinate]]:
        cells: List[Coordinate] = []
        current_x = x
        while True:
            current_x += direction
            pos = (current_x, y)
            if pos in clay:
                return True, cells
            flowing.add(pos)
            cells.append(pos)
            below = (current_x, y + 1)
            if not is_blocked(below):
                flow(current_x, y + 1)
                if not is_blocked(below):
                    return False, cells

    flow(500, 0)
    return flowing, settled


def solve_part1(reservoir: Reservoir) -> int:
    flowing, settled = simulate(reservoir)
    return sum(
        1
        for x, y in flowing | settled
        if reservoir.min_y <= y <= reservoir.max_y
    )


def solve_part2(reservoir: Reservoir) -> int:
    _flowing, settled = simulate(reservoir)
    return sum(1 for _x, y in settled if reservoir.min_y <= y <= reservoir.max_y)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 17.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    data = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
