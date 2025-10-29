from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence


def parse(raw: str) -> list[list[int]]:
    reports: list[list[int]] = []
    for line in raw.splitlines():
        if line.strip():
            reports.append([int(value) for value in line.split()])
    return reports


def is_safe(levels: Sequence[int]) -> bool:
    if len(levels) < 2:
        return True
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
    if all(1 <= d <= 3 for d in diffs):
        return True
    if all(-3 <= d <= -1 for d in diffs):
        return True
    return False


def is_safe_with_dampener(levels: Sequence[int]) -> bool:
    if is_safe(levels):
        return True
    for i in range(len(levels)):
        candidate = levels[:i] + levels[i + 1 :]
        if is_safe(candidate):
            return True
    return False


def solve_part1(reports: Iterable[Sequence[int]]) -> int:
    return sum(1 for report in reports if is_safe(report))


def solve_part2(reports: Iterable[Sequence[int]]) -> int:
    return sum(1 for report in reports if is_safe_with_dampener(report))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 2.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    reports = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(reports)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(reports)}")


if __name__ == "__main__":
    main()
