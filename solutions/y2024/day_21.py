from __future__ import annotations

import argparse
from collections import deque
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Coordinate = tuple[int, int]

NUMERIC_LAYOUT = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

NUMERIC_INVALID = {(0, 3)}

DIRECTION_LAYOUT = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

DIRECTION_INVALID = {(0, 0)}

MOVES = [
    ("^", (0, -1)),
    ("v", (0, 1)),
    ("<", (-1, 0)),
    (">", (1, 0)),
]


def compute_paths(layout: Dict[str, Coordinate], invalid: set[Coordinate]) -> Dict[str, Dict[str, tuple[str, ...]]]:
    keys = list(layout.keys())
    result: Dict[str, Dict[str, tuple[str, ...]]] = {
        start: {target: tuple() for target in keys} for start in keys
    }

    valid_positions = set(layout.values())

    for start_key, start_pos in layout.items():
        queue = deque([start_pos])
        distances: Dict[Coordinate, int] = {start_pos: 0}
        paths: Dict[Coordinate, set[str]] = {start_pos: {""}}

        while queue:
            x, y = queue.popleft()
            for move_char, (dx, dy) in MOVES:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in valid_positions or (nx, ny) in invalid:
                    continue
                new_distance = distances[(x, y)] + 1
                new_sequences = {path + move_char for path in paths[(x, y)]}

                if (nx, ny) not in distances:
                    distances[(nx, ny)] = new_distance
                    paths[(nx, ny)] = new_sequences
                    queue.append((nx, ny))
                elif new_distance == distances[(nx, ny)]:
                    paths[(nx, ny)].update(new_sequences)

        for target_key, target_pos in layout.items():
            sequences = tuple(sorted(path + "A" for path in paths.get(target_pos, {"A"})))
            result[start_key][target_key] = sequences

    return result


NUMERIC_PATHS = compute_paths(NUMERIC_LAYOUT, NUMERIC_INVALID)
DIRECTION_PATHS = compute_paths(DIRECTION_LAYOUT, DIRECTION_INVALID)


@lru_cache(maxsize=None)
def cost_directional_sequence(sequence: str, depth: int) -> int:
    if depth == 0:
        return len(sequence)
    pointer = "A"
    total = 0
    for char in sequence:
        possibilities = DIRECTION_PATHS[pointer][char]
        total += min(cost_directional_sequence(next_sequence, depth - 1) for next_sequence in possibilities)
        pointer = char
    return total


def cost_numeric_code(code: str, depth: int) -> int:
    pointer = "A"
    total = 0
    for char in code:
        possibilities = NUMERIC_PATHS[pointer][char]
        total += min(cost_directional_sequence(sequence, depth) for sequence in possibilities)
        pointer = char
    return total


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def numeric_value(code: str) -> int:
    return int(code[:-1])


def solve_part1(codes: Sequence[str]) -> int:
    total = 0
    for code in codes:
        presses = cost_numeric_code(code, depth=2)
        total += presses * numeric_value(code)
    return total


def solve_part2(codes: Sequence[str]) -> int:
    total = 0
    for code in codes:
        presses = cost_numeric_code(code, depth=25)
        total += presses * numeric_value(code)
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 21.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    codes = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(codes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(codes)}")


if __name__ == "__main__":
    main()
