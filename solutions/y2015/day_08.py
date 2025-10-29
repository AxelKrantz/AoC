from __future__ import annotations

import argparse
import ast
from pathlib import Path


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def solve_part1(strings: list[str]) -> int:
    total_code = sum(len(s) for s in strings)
    total_memory = sum(len(ast.literal_eval(s)) for s in strings)
    return total_code - total_memory


def encode_string(s: str) -> str:
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def solve_part2(strings: list[str]) -> int:
    total_encoded = sum(len(encode_string(s)) for s in strings)
    total_code = sum(len(s) for s in strings)
    return total_encoded - total_code


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 8.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    strings = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(strings)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(strings)}")


if __name__ == "__main__":
    main()
