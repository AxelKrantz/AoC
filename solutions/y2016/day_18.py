from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def next_row(row: str) -> str:
    extended = f".{row}."
    result_chars: list[str] = []
    for i in range(len(row)):
        left, center, right = extended[i : i + 3]
        trap = (left + center + right) in {"^^.", ".^^", "^..", "..^"}
        result_chars.append("^" if trap else ".")
    return "".join(result_chars)


def safe_tiles(first_row: str, rows: int) -> int:
    current = first_row
    total = current.count(".")
    for _ in range(1, rows):
        current = next_row(current)
        total += current.count(".")
    return total


def solve_part1(first_row: str) -> int:
    return safe_tiles(first_row, 40)


def solve_part2(first_row: str) -> int:
    return safe_tiles(first_row, 400000)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 18.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--rows1", type=int, default=40)
    parser.add_argument("--rows2", type=int, default=400000)
    args = parser.parse_args()

    first_row = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {safe_tiles(first_row, args.rows1)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {safe_tiles(first_row, args.rows2)}")


if __name__ == "__main__":
    main()
