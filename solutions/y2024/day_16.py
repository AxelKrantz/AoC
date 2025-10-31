from __future__ import annotations

import argparse
import heapq
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Tuple

Grid = list[list[str]]
Coordinate = tuple[int, int]
Direction = int
State = tuple[int, int, Direction]

DIRECTIONS: list[tuple[int, int]] = [
    (1, 0),   # East
    (0, 1),   # South
    (-1, 0),  # West
    (0, -1),  # North
]

TURN_COST = 1000
STEP_COST = 1


def parse(raw: str) -> Grid:
    return [list(line.strip()) for line in raw.splitlines() if line.strip()]


def find_char(grid: Grid, target: str) -> Coordinate:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == target:
                return x, y
    raise ValueError(f"Character {target!r} not found in grid.")


def in_bounds(grid: Grid, x: int, y: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def is_open(cell: str) -> bool:
    return cell in {".", "S", "E"}


def dijkstra(grid: Grid, start: State) -> Dict[State, int]:
    dist: Dict[State, int] = {}
    queue: list[tuple[int, State]] = [(0, start)]

    while queue:
        cost, state = heapq.heappop(queue)
        if state in dist:
            continue
        dist[state] = cost

        x, y, direction = state

        # Turn left
        left_dir = (direction - 1) % 4
        left_state: State = (x, y, left_dir)
        if left_state not in dist:
            heapq.heappush(queue, (cost + TURN_COST, left_state))

        # Turn right
        right_dir = (direction + 1) % 4
        right_state: State = (x, y, right_dir)
        if right_state not in dist:
            heapq.heappush(queue, (cost + TURN_COST, right_state))

        # Step forward
        dx, dy = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        if in_bounds(grid, nx, ny) and is_open(grid[ny][nx]):
            forward_state: State = (nx, ny, direction)
            if forward_state not in dist:
                heapq.heappush(queue, (cost + STEP_COST, forward_state))

    return dist


def solve_part1(grid: Grid) -> int:
    start_pos = find_char(grid, "S")
    end_pos = find_char(grid, "E")
    start_state: State = (*start_pos, 0)  # Facing East

    dist = dijkstra(grid, start_state)
    best = min(dist.get((*end_pos, direction), float("inf")) for direction in range(4))
    if best == float("inf"):
        raise ValueError("Goal is unreachable.")
    return best


def predecessors(grid: Grid, state: State, dist: Dict[State, int]) -> Iterator[State]:
    x, y, direction = state
    current_cost = dist[state]

    # Turn predecessors
    for delta in (-1, 1):
        prev_dir = (direction - delta) % 4
        prev_state = (x, y, prev_dir)
        if prev_state in dist and dist[prev_state] + TURN_COST == current_cost:
            yield prev_state

    # Forward predecessor
    dx, dy = DIRECTIONS[direction]
    px, py = x - dx, y - dy
    if in_bounds(grid, px, py) and is_open(grid[py][px]):
        prev_state = (px, py, direction)
        if prev_state in dist and dist[prev_state] + STEP_COST == current_cost:
            yield prev_state


def solve_part2(grid: Grid) -> int:
    start_pos = find_char(grid, "S")
    end_pos = find_char(grid, "E")
    start_state: State = (*start_pos, 0)

    dist = dijkstra(grid, start_state)
    end_states = [
        (*end_pos, direction)
        for direction in range(4)
        if (*end_pos, direction) in dist
    ]
    if not end_states:
        raise ValueError("Goal is unreachable.")

    best_total = min(dist[state] for state in end_states)

    stack: list[State] = [state for state in end_states if dist[state] == best_total]
    seen: set[State] = set(stack)

    while stack:
        state = stack.pop()
        for prev in predecessors(grid, state, dist):
            if prev not in seen:
                seen.add(prev)
                stack.append(prev)

    positions = { (x, y) for x, y, _ in seen }
    return len(positions)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 16.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    grid = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(grid)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(grid)}")


if __name__ == "__main__":
    main()
