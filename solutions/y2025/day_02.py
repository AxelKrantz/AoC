from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator
import bisect


@dataclass(frozen=True)
class Range:
    start: int
    end: int  # inclusive


def parse(raw: str) -> list[Range]:
    tokens = [part.strip() for part in raw.strip().split(",") if part.strip()]
    ranges: list[Range] = []
    for token in tokens:
        start_str, end_str = token.split("-")
        ranges.append(Range(int(start_str), int(end_str)))
    return ranges


def merge_ranges(ranges: Iterable[Range]) -> list[Range]:
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    merged: list[Range] = []
    for current in sorted_ranges:
        if not merged or current.start > merged[-1].end + 1:
            merged.append(current)
        else:
            last = merged[-1]
            merged[-1] = Range(last.start, max(last.end, current.end))
    return merged


def repeated_double_candidates(length: int) -> Iterator[int]:
    """Yield numbers whose decimal representation is some k-digit sequence repeated twice."""
    if length % 2 == 1:
        return iter(())
    half = length // 2
    base = 10 ** (half - 1)
    limit = 10**half
    for prefix in range(base, limit):
        yield prefix * (10**half) + prefix


def invalid_ids_in_range(rng: Range) -> Iterator[int]:
    min_len = len(str(rng.start))
    max_len = len(str(rng.end))
    for length in range(min_len + (min_len % 2), max_len + 1, 2):
        for candidate in repeated_double_candidates(length):
            if candidate < rng.start:
                continue
            if candidate > rng.end:
                break
            yield candidate


def solve_part1(ranges: Iterable[Range]) -> int:
    merged = merge_ranges(ranges)
    total = 0
    for rng in merged:
        total += sum(invalid_ids_in_range(rng))
    return total


# Part 2 helpers
_invalid_cache: dict[int, list[int]] = {}


def invalid_numbers_of_length(length: int) -> list[int]:
    if length in _invalid_cache:
        return _invalid_cache[length]
    numbers: set[int] = set()
    for base_length in range(1, length):
        repeats = length // base_length
        if repeats < 2 or length % base_length != 0:
            continue
        start = 10 ** (base_length - 1)
        end = 10**base_length
        for prefix in range(start, end):
            candidate = int(str(prefix) * repeats)
            numbers.add(candidate)
    ordered = sorted(numbers)
    _invalid_cache[length] = ordered
    return ordered


def sum_invalid_in_range(rng: Range) -> int:
    total = 0
    min_len = len(str(rng.start))
    max_len = len(str(rng.end))
    for length in range(min_len, max_len + 1):
        numbers = invalid_numbers_of_length(length)
        if not numbers:
            continue
        low = max(rng.start, 10 ** (length - 1))
        high = min(rng.end, 10**length - 1)
        if low > high:
            continue
        left = bisect.bisect_left(numbers, low)
        right = bisect.bisect_right(numbers, high)
        total += sum(numbers[left:right])
    return total


def solve_part2(ranges: Iterable[Range]) -> int:
    merged = merge_ranges(ranges)
    return sum(sum_invalid_in_range(rng) for rng in merged)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 2.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    ranges = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(ranges)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(ranges)}")


if __name__ == "__main__":
    main()
