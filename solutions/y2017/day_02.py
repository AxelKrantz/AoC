from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> list[list[int]]:
    rows: list[list[int]] = []
    for line in raw.strip().splitlines():
        if line.strip():
            rows.append([int(value) for value in line.split()])
    return rows


def solve_part1(rows: list[list[int]]) -> int:
    return sum(max(row) - min(row) for row in rows)


def solve_part2(rows: list[list[int]]) -> int:
    total = 0
    for row in rows:
        for i, a in enumerate(row):
            for j, b in enumerate(row):
                if i == j:
                    continue
                if a % b == 0:
                    total += a // b
                    break
            else:
                continue
            break
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 2.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    rows = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(rows)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(rows)}")


if __name__ == "__main__":
    main()
