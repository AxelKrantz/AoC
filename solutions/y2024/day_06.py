from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple

DirectionIndex = int


class GuardMap(NamedTuple):
    grid: list[list[str]]
    start: tuple[int, int]
    direction: DirectionIndex


FACING_TO_INDEX: dict[str, DirectionIndex] = {
    "^": 0,
    ">": 1,
    "v": 2,
    "<": 3,
}

# Order is important: rotate right is (index + 1) % 4.
DIRECTIONS: list[tuple[int, int]] = [
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
]


def parse(raw: str) -> GuardMap:
    grid = [list(line.strip()) for line in raw.splitlines() if line.strip()]
    start: tuple[int, int] | None = None
    direction: DirectionIndex | None = None

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in FACING_TO_INDEX:
                start = (r, c)
                direction = FACING_TO_INDEX[ch]
                row[c] = "."  # Treat the starting position as empty floor for simulation.
                break
        if start is not None:
            break

    if start is None or direction is None:
        raise ValueError("Guard starting position not found in map.")

    return GuardMap(grid=grid, start=start, direction=direction)


def simulate(
    guard_map: GuardMap, extra_obstruction: tuple[int, int] | None = None
) -> tuple[set[tuple[int, int]], bool, bool]:
    grid, (row, col), direction = guard_map
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    visited_positions: set[tuple[int, int]] = {(row, col)}
    seen_states: set[tuple[int, int, int]] = {(row, col, direction)}

    while True:
        dr, dc = DIRECTIONS[direction]
        next_row = row + dr
        next_col = col + dc

        if not (0 <= next_row < rows and 0 <= next_col < cols):
            return visited_positions, True, False  # Guard left the map.

        if grid[next_row][next_col] == "#" or (
            extra_obstruction is not None
            and (next_row, next_col) == extra_obstruction
        ):
            direction = (direction + 1) % 4
            state = (row, col, direction)
            if state in seen_states:
                return visited_positions, False, True
            seen_states.add(state)
            continue

        row, col = next_row, next_col
        visited_positions.add((row, col))
        state = (row, col, direction)
        if state in seen_states:
            return visited_positions, False, True
        seen_states.add(state)


def solve_part1(guard_map: GuardMap) -> int:
    visited, exited, looped = simulate(guard_map)
    if looped:
        raise RuntimeError("Unexpected loop detected during part 1 simulation.")
    if not exited:
        raise RuntimeError("Guard did not leave the map as expected in part 1.")
    return len(visited)


def solve_part2(guard_map: GuardMap) -> int:
    visited, exited, looped = simulate(guard_map)
    if looped:
        raise RuntimeError("Unexpected loop detected during initial simulation.")
    if not exited:
        raise RuntimeError("Guard should leave the map without additional obstructions.")

    start_position = guard_map.start
    total = 0

    for candidate in visited:
        if candidate == start_position:
            continue
        _, _, loop_detected = simulate(guard_map, extra_obstruction=candidate)
        if loop_detected:
            total += 1

    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 6.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    guard_map = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(guard_map)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(guard_map)}")


if __name__ == "__main__":
    main()
