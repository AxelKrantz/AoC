from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse(raw: str) -> Any:
    return json.loads(raw.strip())


def sum_numbers(data: Any) -> int:
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum(sum_numbers(item) for item in data)
    if isinstance(data, dict):
        return sum(sum_numbers(value) for value in data.values())
    return 0


def sum_numbers_skip_red(data: Any) -> int:
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum(sum_numbers_skip_red(item) for item in data)
    if isinstance(data, dict):
        if "red" in data.values():
            return 0
        return sum(sum_numbers_skip_red(value) for value in data.values())
    return 0


def solve_part1(document: Any) -> int:
    return sum_numbers(document)


def solve_part2(document: Any) -> int:
    return sum_numbers_skip_red(document)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 12.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    document = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(document)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(document)}")


if __name__ == "__main__":
    main()
