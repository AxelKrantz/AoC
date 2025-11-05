from __future__ import annotations

import argparse
import re
from pathlib import Path


INITIAL_CODE = 20151125
MULTIPLIER = 252533
MODULUS = 33554393


def parse(raw: str) -> tuple[int, int]:
    numbers = [int(value) for value in re.findall(r"\d+", raw)]
    if len(numbers) < 2:
        raise ValueError("Row and column could not be parsed from input.")
    row, column = numbers[-2], numbers[-1]
    return row, column


def code_index(row: int, column: int) -> int:
    diagonal = row + column - 1
    numbers_before = diagonal * (diagonal - 1) // 2
    return numbers_before + column


def compute_code(row: int, column: int) -> int:
    index = code_index(row, column)
    exponent = index - 1
    return (INITIAL_CODE * pow(MULTIPLIER, exponent, MODULUS)) % MODULUS


def solve_part1(position: tuple[int, int]) -> int:
    row, column = position
    return compute_code(row, column)


def solve_part2(position: tuple[int, int]) -> int:
    return solve_part1(position)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 25.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    position = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(position)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(position)}")


if __name__ == "__main__":
    main()
