from __future__ import annotations

import argparse
import heapq
from pathlib import Path
from typing import Iterator, List, Sequence, Tuple

Bot = tuple[int, int, int, int]


def parse(raw: str) -> List[Bot]:
    bots: list[Bot] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        pos_part, radius_part = line.split(", ")
        x_str, y_str, z_str = pos_part[5:-1].split(",")
        bots.append((int(x_str), int(y_str), int(z_str), int(radius_part[2:])))
    return bots


def manhattan(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def solve_part1(bots: Sequence[Bot]) -> int:
    strongest = max(bots, key=lambda bot: bot[3])
    sx, sy, sz, sr = strongest
    count = 0
    for x, y, z, _r in bots:
        if manhattan((x, y, z), (sx, sy, sz)) <= sr:
            count += 1
    return count


Cube = tuple[int, int, int, int]


def cube_distance_to_origin(cube: Cube) -> int:
    x, y, z, size = cube
    max_x = x + size - 1
    max_y = y + size - 1
    max_z = z + size - 1

    def axis_distance(min_coord: int, max_coord: int) -> int:
        if max_coord < 0:
            return -max_coord
        if min_coord > 0:
            return min_coord
        return 0

    return axis_distance(x, max_x) + axis_distance(y, max_y) + axis_distance(z, max_z)


def distance_bot_to_cube(bot: Bot, cube: Cube) -> int:
    bx, by, bz, _ = bot
    x, y, z, size = cube
    max_x = x + size - 1
    max_y = y + size - 1
    max_z = z + size - 1

    dx = 0
    if bx < x:
        dx = x - bx
    elif bx > max_x:
        dx = bx - max_x

    dy = 0
    if by < y:
        dy = y - by
    elif by > max_y:
        dy = by - max_y

    dz = 0
    if bz < z:
        dz = z - bz
    elif bz > max_z:
        dz = bz - max_z

    return dx + dy + dz


def bots_in_cube(bots: Sequence[Bot], cube: Cube) -> int:
    count = 0
    for bot in bots:
        if distance_bot_to_cube(bot, cube) <= bot[3]:
            count += 1
    return count


def initial_cube(bots: Sequence[Bot]) -> Cube:
    min_coord = min(min(x, y, z) for x, y, z, _ in bots)
    max_coord = max(max(x, y, z) for x, y, z, _ in bots)
    size = 1
    while size < max_coord - min_coord:
        size *= 2
    return (min_coord, min_coord, min_coord, size)


def solve_part2(bots: Sequence[Bot]) -> int:
    cube = initial_cube(bots)
    heap: list[tuple[int, int, int, Cube]] = []
    count = bots_in_cube(bots, cube)
    heapq.heappush(heap, (-count, cube_distance_to_origin(cube), cube[3], cube))

    while heap:
        neg_count, distance, size, cube = heapq.heappop(heap)
        count = -neg_count
        x, y, z, size = cube

        if size == 1:
            return distance

        half = size // 2
        for dx in (0, half):
            for dy in (0, half):
                for dz in (0, half):
                    sub_cube = (x + dx, y + dy, z + dz, half)
                    sub_count = bots_in_cube(bots, sub_cube)
                    heapq.heappush(
                        heap,
                        (-sub_count, cube_distance_to_origin(sub_cube), half, sub_cube),
                    )

    raise RuntimeError("No solution found for Part 2.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 23.")
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
