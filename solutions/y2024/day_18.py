from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

Coordinate = tuple[int, int]


def parse(raw: str) -> list[Coordinate]:
    coordinates: list[Coordinate] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str = line.split(",")
        coordinates.append((int(x_str), int(y_str)))
    return coordinates


def shortest_path_length(
    blocked: set[Coordinate], grid_size: int
) -> Optional[int]:
    start = (0, 0)
    target = (grid_size, grid_size)

    if start in blocked or target in blocked:
        return None

    queue: deque[tuple[Coordinate, int]] = deque([(start, 0)])
    visited: set[Coordinate] = {start}

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == target:
            return steps
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx <= grid_size and 0 <= ny <= grid_size):
                continue
            coord = (nx, ny)
            if coord in blocked or coord in visited:
                continue
            visited.add(coord)
            queue.append((coord, steps + 1))
    return None


def solve_part1(coordinates: Sequence[Coordinate], grid_size: int = 70, byte_limit: int = 1024) -> int:
    blocked = set(coordinates[:byte_limit])
    result = shortest_path_length(blocked, grid_size)
    if result is None:
        raise ValueError("No path exists after specified bytes have fallen.")
    return result


def solve_part2(coordinates: Sequence[Coordinate], grid_size: int = 70) -> str:
    total_bytes = len(coordinates)

    def path_exists(byte_count: int) -> bool:
        blocked = set(coordinates[:byte_count])
        return shortest_path_length(blocked, grid_size) is not None

    low = 0
    high = total_bytes
    while low < high:
        mid = (low + high) // 2
        if path_exists(mid):
            low = mid + 1
        else:
            high = mid

    if low == 0:
        raise ValueError("Path is blocked even before any bytes fall.")
    blocking_coordinate = coordinates[low - 1]
    return f"{blocking_coordinate[0]},{blocking_coordinate[1]}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 18.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--grid", type=int, default=70, help="Grid size (default 70 for coordinates 0..70).")
    parser.add_argument("--bytes", type=int, default=1024, help="Number of initial bytes to simulate for part 1.")
    args = parser.parse_args()

    coordinates = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(coordinates, grid_size=args.grid, byte_limit=args.bytes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(coordinates, grid_size=args.grid)}")


if __name__ == "__main__":
    main()
