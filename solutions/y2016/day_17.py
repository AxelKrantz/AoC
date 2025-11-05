from __future__ import annotations

import argparse
import collections
import hashlib
from pathlib import Path
from typing import Deque, Optional

MOVES = [
    ("U", (0, -1)),
    ("D", (0, 1)),
    ("L", (-1, 0)),
    ("R", (1, 0)),
]


def parse(raw: str) -> str:
    return raw.strip()


def open_doors(passcode: str, path: str) -> list[str]:
    digest = hashlib.md5(f"{passcode}{path}".encode("utf-8")).hexdigest()
    result: list[str] = []
    for (direction, _), char in zip(MOVES, digest[:4]):
        if char in "bcdef":
            result.append(direction)
    return result


def move(position: tuple[int, int], direction: str) -> tuple[int, int]:
    for dir_code, (dx, dy) in MOVES:
        if dir_code == direction:
            return position[0] + dx, position[1] + dy
    raise ValueError(f"Unknown direction: {direction}")


def in_bounds(position: tuple[int, int]) -> bool:
    x, y = position
    return 0 <= x < 4 and 0 <= y < 4


def shortest_path(passcode: str) -> Optional[str]:
    start = (0, 0)
    queue: Deque[tuple[tuple[int, int], str]] = collections.deque([(start, "")])
    while queue:
        position, path = queue.popleft()
        if position == (3, 3):
            return path
        for direction in open_doors(passcode, path):
            new_position = move(position, direction)
            if in_bounds(new_position):
                queue.append((new_position, path + direction))
    return None


def longest_path_length(passcode: str) -> int:
    start = (0, 0)
    queue: Deque[tuple[tuple[int, int], str]] = collections.deque([(start, "")])
    longest = 0
    while queue:
        position, path = queue.popleft()
        if position == (3, 3):
            longest = max(longest, len(path))
            continue
        for direction in open_doors(passcode, path):
            new_position = move(position, direction)
            if in_bounds(new_position):
                queue.append((new_position, path + direction))
    return longest


def solve_part1(passcode: str) -> str:
    result = shortest_path(passcode)
    if result is None:
        raise ValueError("No path to vault.")
    return result


def solve_part2(passcode: str) -> int:
    return longest_path_length(passcode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 17.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    passcode = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(passcode)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(passcode)}")


if __name__ == "__main__":
    main()
