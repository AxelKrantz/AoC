from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> str:
    """Return the raw sequence stripped of trailing whitespace."""
    return raw.strip()


def solve_part1(sequence: str) -> int:
    """Calculate the final floor after processing the entire sequence."""
    deltas = {"(": 1, ")": -1}
    return sum(deltas[char] for char in sequence)


def solve_part2(sequence: str) -> int:
    """Return the first position (1-based) where Santa enters the basement."""
    deltas = {"(": 1, ")": -1}
    floor = 0
    for index, char in enumerate(sequence, start=1):
        floor += deltas[char]
        if floor == -1:
            return index
    raise ValueError("Basement was never reached.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 1.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument(
        "--part",
        choices={"1", "2", "both"},
        default="both",
        help="Choose which part to evaluate.",
    )
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    sequence = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(sequence)}")
    if args.part in {"2", "both"}:
        try:
            result = solve_part2(sequence)
        except ValueError as error:
            print(f"Part 2 error: {error}")
        else:
            print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
