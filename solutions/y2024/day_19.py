from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


def parse(raw: str) -> tuple[list[str], list[str]]:
    patterns_section, designs_section = raw.strip().split("\n\n", 1)
    patterns = [pattern.strip() for pattern in patterns_section.split(",")]
    designs = [line.strip() for line in designs_section.splitlines() if line.strip()]
    return patterns, designs


def build_prefix_map(patterns: Sequence[str]) -> Dict[str, list[str]]:
    prefix_map: Dict[str, list[str]] = {}
    for pattern in patterns:
        if not pattern:
            continue
        prefix_map.setdefault(pattern[0], []).append(pattern)
    return prefix_map


def count_arrangements(patterns: Sequence[str], design: str) -> int:
    prefix_map = build_prefix_map(patterns)

    @lru_cache(maxsize=None)
    def helper(remaining: str) -> int:
        if not remaining:
            return 1
        total = 0
        first_char = remaining[0]
        for pattern in prefix_map.get(first_char, []):
            if remaining.startswith(pattern):
                total += helper(remaining[len(pattern):])
        return total

    return helper(design)


def solve_part1(patterns: Sequence[str], designs: Sequence[str]) -> int:
    return sum(1 for design in designs if count_arrangements(patterns, design) > 0)


def solve_part2(patterns: Sequence[str], designs: Sequence[str]) -> int:
    return sum(count_arrangements(patterns, design) for design in designs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 19.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    patterns, designs = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(patterns, designs)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(patterns, designs)}")


if __name__ == "__main__":
    main()
