from __future__ import annotations

import argparse
import collections
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, Dict, Iterable, List, Tuple

NODE_RE = re.compile(
    r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+"
    r"(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T"
)


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int


def parse(raw: str) -> list[Node]:
    nodes: list[Node] = []
    for line in raw.strip().splitlines():
        match = NODE_RE.search(line)
        if not match:
            continue
        nodes.append(
            Node(
                x=int(match.group("x")),
                y=int(match.group("y")),
                size=int(match.group("size")),
                used=int(match.group("used")),
                avail=int(match.group("avail")),
            )
        )
    return nodes


def solve_part1(nodes: Iterable[Node]) -> int:
    nodes_list = list(nodes)
    count = 0
    for a in nodes_list:
        if a.used == 0:
            continue
        for b in nodes_list:
            if a == b:
                continue
            if a.used <= b.avail:
                count += 1
    return count


def solve_part2(nodes: Iterable[Node]) -> int:
    nodes_list = list(nodes)
    grid: Dict[Tuple[int, int], Node] = {(node.x, node.y): node for node in nodes_list}
    max_x = max(node.x for node in nodes_list)

    empty = next(node for node in nodes_list if node.used == 0)
    empty_pos = (empty.x, empty.y)

    wall_threshold = empty.size
    walls = {
        (node.x, node.y)
        for node in nodes_list
        if node.used > wall_threshold
    }

    target = (max_x, 0)
    steps_to_target = shortest_path(empty_pos, (target[0] - 1, target[1]), walls, grid)

    total_steps = steps_to_target
    total_steps += 1
    total_steps += 5 * (target[0] - 1)
    return total_steps


def shortest_path(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    walls: set[Tuple[int, int]],
    grid: Dict[Tuple[int, int], Node],
) -> int:
    queue: Deque[Tuple[Tuple[int, int], int]] = collections.deque([(start, 0)])
    seen = {start}
    max_x = max(coord[0] for coord in grid)
    max_y = max(coord[1] for coord in grid)

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == goal:
            return steps
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx <= max_x and 0 <= ny <= max_y):
                continue
            if (nx, ny) in walls:
                continue
            if (nx, ny) in seen:
                continue
            seen.add((nx, ny))
            queue.append(((nx, ny), steps + 1))
    raise ValueError("Path not found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 22.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    nodes = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(nodes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(nodes)}")


if __name__ == "__main__":
    main()
