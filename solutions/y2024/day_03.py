from __future__ import annotations

import argparse
import re
from pathlib import Path

MUL_RE = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def parse(raw: str) -> str:
    return raw


def evaluate_enabled_products(program: str, *, respect_switches: bool) -> int:
    enabled = True
    total = 0
    index = 0
    while index < len(program):
        if respect_switches and program.startswith("do()", index):
            enabled = True
            index += 4
            continue
        if respect_switches and program.startswith("don't()", index):
            enabled = False
            index += 7
            continue
        match = MUL_RE.match(program, index)
        if match:
            if enabled:
                a, b = match.groups()
                total += int(a) * int(b)
            index = match.end()
        else:
            index += 1
    return total


def solve_part1(program: str) -> int:
    return evaluate_enabled_products(program, respect_switches=False)


def solve_part2(program: str) -> int:
    return evaluate_enabled_products(program, respect_switches=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 3.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    program = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(program)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(program)}")


if __name__ == "__main__":
    main()
