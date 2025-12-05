from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Range:
    start: int
    end: int  # inclusive


def parse(raw: str) -> tuple[list[Range], list[int]]:
    try:
        ranges_block, ids_block = raw.strip().split("\n\n", 1)
    except ValueError as error:
        raise ValueError("Input must contain two sections separated by a blank line.") from error

    ranges = []
    for line in ranges_block.splitlines():
        start_str, end_str = line.split("-")
        ranges.append(Range(int(start_str), int(end_str)))

    ids = [int(line) for line in ids_block.splitlines() if line.strip()]
    return ranges, ids


def merge_ranges(ranges: Iterable[Range]) -> list[Range]:
    """Merge overlapping and contiguous inclusive ranges."""
    ordered = sorted(ranges, key=lambda r: r.start)
    merged: list[Range] = []
    for current in ordered:
        if not merged or current.start > merged[-1].end + 1:
            merged.append(Range(current.start, current.end))
        else:
            last = merged[-1]
            merged[-1] = Range(last.start, max(last.end, current.end))
    return merged


def count_ids_in_ranges(ids: Sequence[int], merged_ranges: Sequence[Range]) -> int:
    """Count how many IDs fall inside any of the merged ranges."""
    import bisect

    starts = [r.start for r in merged_ranges]
    count = 0
    for value in ids:
        idx = bisect.bisect_right(starts, value) - 1
        if idx >= 0:
            candidate = merged_ranges[idx]
            if candidate.start <= value <= candidate.end:
                count += 1
    return count


def solve_part1(parsed: tuple[list[Range], list[int]]) -> int:
    ranges, ids = parsed
    merged = merge_ranges(ranges)
    return count_ids_in_ranges(ids, merged)


def solve_part2(ranges: Sequence[Range]) -> int:
    merged = merge_ranges(ranges)
    return sum(r.end - r.start + 1 for r in merged)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 5.")
    parser.add_argument("input_path", type=Path, help="Path to puzzle input.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    ranges, ids = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1((ranges, ids))}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(ranges)}")


if __name__ == "__main__":
    main()
