from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

START_POSITION = 50
DIAL_SIZE = 100


@dataclass(frozen=True)
class Rotation:
    direction: str
    distance: int


def parse(raw: str) -> list[Rotation]:
    rotations: list[Rotation] = []
    for line in raw.splitlines():
        token = line.strip()
        if not token:
            continue
        direction = token[0]
        distance = int(token[1:])
        rotations.append(Rotation(direction, distance))
    return rotations


def apply_rotation(position: int, rotation: Rotation) -> int:
    offset = rotation.distance % DIAL_SIZE
    if rotation.direction == "L":
        offset = -offset
    elif rotation.direction == "R":
        offset = offset
    else:
        raise ValueError(f"Unknown direction {rotation.direction!r}")
    return (position + offset) % DIAL_SIZE


def solve_part1(rotations: Sequence[Rotation]) -> int:
    position = START_POSITION
    zero_hits = 0
    for rotation in rotations:
        position = apply_rotation(position, rotation)
        if position == 0:
            zero_hits += 1
    return zero_hits


def zero_hits_during_rotation(position: int, rotation: Rotation) -> int:
    """Count how many clicks during a rotation land on zero."""
    if rotation.distance == 0:
        return 0
    # Determine the first step index (1-based) that reaches zero, then count every 100th step.
    if rotation.direction == "R":
        first_hit = (DIAL_SIZE - position) % DIAL_SIZE or DIAL_SIZE
    elif rotation.direction == "L":
        first_hit = position or DIAL_SIZE
    else:
        raise ValueError(f"Unknown direction {rotation.direction!r}")
    if first_hit > rotation.distance:
        return 0
    return 1 + (rotation.distance - first_hit) // DIAL_SIZE


def solve_part2(rotations: Sequence[Rotation]) -> int:
    position = START_POSITION
    zero_hits = 0
    for rotation in rotations:
        zero_hits += zero_hits_during_rotation(position, rotation)
        position = apply_rotation(position, rotation)
    return zero_hits


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 1.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    rotations = parse(raw)

    if args.part == "1":
        print(f"Part 1: {solve_part1(rotations)}")
    elif args.part == "2":
        print(f"Part 2: {solve_part2(rotations)}")
    else:
        print(f"Part 1: {solve_part1(rotations)}")
        print(f"Part 2: {solve_part2(rotations)}")


if __name__ == "__main__":
    main()
