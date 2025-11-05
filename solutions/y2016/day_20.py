from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

Range = Tuple[int, int]


def parse(raw: str) -> List[Range]:
    ranges: list[Range] = []
    for line in raw.strip().splitlines():
        start_str, end_str = line.strip().split("-")
        ranges.append((int(start_str), int(end_str)))
    return ranges


def merge_ranges(ranges: Sequence[Range]) -> List[Range]:
    if not ranges:
        return []
    sorted_ranges = sorted(ranges)
    merged: list[Range] = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def lowest_allowed(ranges: Sequence[Range], max_value: int) -> int:
    merged = merge_ranges(ranges)
    candidate = 0
    for start, end in merged:
        if candidate < start:
            return candidate
        candidate = max(candidate, end + 1)
        if candidate > max_value:
            break
    if candidate <= max_value:
        return candidate
    raise ValueError("No allowed address found.")


def count_allowed(ranges: Sequence[Range], max_value: int) -> int:
    merged = merge_ranges(ranges)
    allowed = 0
    candidate = 0
    for start, end in merged:
        if candidate < start:
            allowed += start - candidate
        candidate = max(candidate, end + 1)
        if candidate > max_value:
            return allowed
    if candidate <= max_value:
        allowed += max_value - candidate + 1
    return allowed


def solve_part1(ranges: Sequence[Range], max_value: int = 4294967295) -> int:
    return lowest_allowed(ranges, max_value)


def solve_part2(ranges: Sequence[Range], max_value: int = 4294967295) -> int:
    return count_allowed(ranges, max_value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 20.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--max-value", type=int, default=4294967295)
    args = parser.parse_args()

    ranges = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(ranges, max_value=args.max_value)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(ranges, max_value=args.max_value)}")


if __name__ == "__main__":
    main()
