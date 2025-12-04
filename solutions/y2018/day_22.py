from __future__ import annotations

import argparse
import heapq
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, Iterator, Tuple

Point = tuple[int, int]
ParsedInput = tuple[int, Point]

TORCH = 0
CLIMBING_GEAR = 1
NEITHER = 2

REGION_TOOLS = {
    0: {TORCH, CLIMBING_GEAR},  # rocky
    1: {CLIMBING_GEAR, NEITHER},  # wet
    2: {TORCH, NEITHER},  # narrow
}


def parse(raw: str) -> ParsedInput:
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    depth = int(lines[0].split(":")[1].strip())
    target_part = lines[1].split(":")[1].strip()
    target_x, target_y = (int(value) for value in target_part.split(","))
    return depth, (target_x, target_y)


def cave_factory(depth: int, target: Point):
    @lru_cache(maxsize=None)
    def erosion_level(x: int, y: int) -> int:
        if (x, y) in {(0, 0), target}:
            geologic_index = 0
        elif y == 0:
            geologic_index = x * 16807
        elif x == 0:
            geologic_index = y * 48271
        else:
            geologic_index = erosion_level(x - 1, y) * erosion_level(x, y - 1)
        return (geologic_index + depth) % 20183

    def region_type(x: int, y: int) -> int:
        return erosion_level(x, y) % 3

    return erosion_level, region_type


def solve_part1(data: ParsedInput) -> int:
    depth, target = data
    erosion_level, region_type = cave_factory(depth, target)
    target_x, target_y = target
    risk = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            risk += region_type(x, y)
    return risk


def neighbors(point: Point) -> Iterator[Point]:
    x, y = point
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if nx >= 0 and ny >= 0:
            yield nx, ny


def solve_part2(data: ParsedInput, margin: int = 50) -> int:
    depth, target = data
    erosion_level, region_type = cave_factory(depth, target)
    target_x, target_y = target
    max_x = target_x + margin
    max_y = target_y + margin

    start_state = (0, 0, TORCH)
    target_state = (target_x, target_y, TORCH)

    heap: list[tuple[int, int, int, int]] = [(0, *start_state)]
    best_time: Dict[tuple[int, int, int], int] = {start_state: 0}

    while heap:
        time, x, y, tool = heapq.heappop(heap)
        state = (x, y, tool)
        if time > best_time.get(state, float("inf")):
            continue
        if state == target_state:
            return time

        current_region = region_type(x, y)
        allowed_tools = REGION_TOOLS[current_region]

        for new_tool in allowed_tools:
            if new_tool == tool:
                continue
            new_state = (x, y, new_tool)
            new_time = time + 7
            if new_time < best_time.get(new_state, float("inf")):
                best_time[new_state] = new_time
                heapq.heappush(heap, (new_time, x, y, new_tool))

        for nx, ny in neighbors((x, y)):
            if nx > max_x or ny > max_y:
                continue
            next_region = region_type(nx, ny)
            if tool not in REGION_TOOLS[next_region]:
                continue
            new_state = (nx, ny, tool)
            new_time = time + 1
            if new_time < best_time.get(new_state, float("inf")):
                best_time[new_state] = new_time
                heapq.heappush(heap, (new_time, nx, ny, tool))

    raise RuntimeError("Unable to reach target with given constraints.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 22.")
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
