from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

Grid = list[list[str]]
Coordinate = tuple[int, int]

DIRECTIONS = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


def parse(raw: str) -> tuple[Grid, str]:
    map_section, moves_section = raw.strip().split("\n\n", 1)
    grid = [list(line.strip()) for line in map_section.splitlines()]
    moves = "".join(line.strip() for line in moves_section.splitlines())
    return grid, moves


def find_robot(grid: Grid) -> Coordinate:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                return x, y
    raise ValueError("Robot position not found.")


def attempt_push_part1(grid: Grid, origin: Coordinate, direction: Coordinate) -> bool:
    dx, dy = direction
    x, y = origin
    chain: list[Coordinate] = []

    nx, ny = x + dx, y + dy
    while True:
        cell = grid[ny][nx]
        if cell == "#":
            return False
        if cell == ".":
            break
        if cell == "O":
            chain.append((nx, ny))
            nx += dx
            ny += dy
            continue
        raise ValueError(f"Unexpected cell {cell!r} during push.")

    # Place a box in the free space we found.
    grid[ny][nx] = "O"

    # Shift each box in the chain forward.
    for bx, by in reversed(chain):
        grid[by + dy][bx + dx] = "O"
        grid[by][bx] = "."

    # Move robot after the boxes have been shifted.
    rx, ry = origin
    grid[ry][rx] = "."
    grid[ry + dy][rx + dx] = "@"
    return True


def perform_moves_part1(grid: Grid, moves: Sequence[str]) -> Grid:
    robot = find_robot(grid)
    for move in moves:
        dx, dy = DIRECTIONS[move]
        x, y = robot
        nx, ny = x + dx, y + dy
        cell = grid[ny][nx]
        if cell == "#":
            continue
        if cell == ".":
            grid[y][x] = "."
            grid[ny][nx] = "@"
            robot = (nx, ny)
            continue
        if cell == "O":
            if attempt_push_part1(grid, robot, (dx, dy)):
                robot = (nx, ny)
            continue
        raise ValueError(f"Unexpected cell {cell!r} during move.")
    return grid


def gps_sum(grid: Grid) -> int:
    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "O":
                total += 100 * y + x
    return total


def solve_part1(grid: Grid, moves: str) -> int:
    final_grid = perform_moves_part1(grid, moves)
    return gps_sum(final_grid)


def expand_grid(grid: Grid) -> Grid:
    mapping = {
        "#": "##",
        ".": "..",
        "O": "[]",
        "@": "@.",
    }
    expanded: Grid = []
    for row in grid:
        new_row: list[str] = []
        for cell in row:
            if cell not in mapping:
                raise ValueError(f"Unexpected cell {cell!r} during expansion.")
            new_row.extend(mapping[cell])
        expanded.append(new_row)
    return expanded


def attempt_push_horizontal(grid: Grid, origin: Coordinate, direction: Coordinate) -> bool:
    dx, dy = direction
    if dy != 0:
        raise ValueError("Horizontal push received non-horizontal direction.")

    robot_x, robot_y = origin
    cx, cy = robot_x + dx, robot_y + dy

    ordered_positions: list[Coordinate] = []
    seen: set[Coordinate] = set()

    while True:
        cell = grid[cy][cx]
        if cell == "#":
            return False
        if cell == ".":
            break
        if cell == "[":
            for pos in ((cx, cy), (cx + 1, cy)):
                if pos not in seen:
                    ordered_positions.append(pos)
                    seen.add(pos)
            cx += 1  # skip the right half
        elif cell == "]":
            for pos in ((cx - 1, cy), (cx, cy)):
                if pos not in seen:
                    ordered_positions.append(pos)
                    seen.add(pos)
            cx -= 1  # skip the left half
        else:
            raise ValueError(f"Unexpected cell {cell!r} during horizontal push.")
        cx += dx

    if dx > 0:
        move_order = sorted(ordered_positions, key=lambda pos: pos[0], reverse=True)
    else:
        move_order = sorted(ordered_positions, key=lambda pos: pos[0])

    for px, py in move_order:
        grid[py][px + dx] = grid[py][px]
        grid[py][px] = "."

    grid[robot_y][robot_x] = "."
    grid[robot_y + dy][robot_x + dx] = "@"
    return True


def attempt_push_vertical(grid: Grid, origin: Coordinate, direction: Coordinate) -> bool:
    dx, dy = direction
    if dx != 0:
        raise ValueError("Vertical push received non-vertical direction.")

    to_visit: list[Coordinate] = [(origin[0] + dx, origin[1] + dy)]
    visited: set[Coordinate] = set()
    moving_cells: set[Coordinate] = set()

    while to_visit:
        cx, cy = to_visit.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        cell = grid[cy][cx]
        if cell == "#":
            return False
        if cell == ".":
            continue
        if cell not in {"[", "]"}:
            raise ValueError(f"Unexpected cell {cell!r} during vertical push.")

        left_x = cx if cell == "[" else cx - 1
        right_x = left_x + 1

        for pos in ((left_x, cy), (right_x, cy)):
            moving_cells.add(pos)
            to_visit.append((pos[0], pos[1] + dy))

    if dy > 0:
        move_order = sorted(moving_cells, key=lambda pos: pos[1], reverse=True)
    else:
        move_order = sorted(moving_cells, key=lambda pos: pos[1])

    for px, py in move_order:
        grid[py + dy][px] = grid[py][px]
        grid[py][px] = "."

    robot_x, robot_y = origin
    grid[robot_y][robot_x] = "."
    grid[robot_y + dy][robot_x + dx] = "@"
    return True


def perform_moves_part2(grid: Grid, moves: Sequence[str]) -> Grid:
    robot = find_robot(grid)
    for move in moves:
        dx, dy = DIRECTIONS[move]
        x, y = robot
        nx, ny = x + dx, y + dy
        cell = grid[ny][nx]
        if cell == "#":
            continue
        if cell == ".":
            grid[y][x] = "."
            grid[ny][nx] = "@"
            robot = (nx, ny)
            continue
        if cell in {"[", "]"}:
            pushed = (
                attempt_push_horizontal(grid, robot, (dx, dy))
                if dy == 0
                else attempt_push_vertical(grid, robot, (dx, dy))
            )
            if pushed:
                robot = (nx, ny)
            continue
        raise ValueError(f"Unexpected cell {cell!r} during wide move.")
    return grid


def gps_sum_wide(grid: Grid) -> int:
    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "[":
                total += 100 * y + x
    return total


def solve_part2(grid: Grid, moves: str) -> int:
    wide_grid = expand_grid(grid)
    final_grid = perform_moves_part2(wide_grid, moves)
    return gps_sum_wide(final_grid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 15.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    grid, moves = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1([row[:] for row in grid], moves)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2([row[:] for row in grid], moves)}")


if __name__ == "__main__":
    main()
