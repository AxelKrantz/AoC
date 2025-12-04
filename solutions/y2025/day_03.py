from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def best_number(bank: str, length: int) -> int:
    """Return lexicographically largest subsequence of given length."""
    stack: list[str] = []
    n = len(bank)
    for i, ch in enumerate(bank):
        remaining = n - i
        while stack and ch > stack[-1] and len(stack) - 1 + remaining >= length:
            stack.pop()
        if len(stack) < length:
            stack.append(ch)
    return int("".join(stack))


def solve_part1(banks: Sequence[str]) -> int:
    return sum(best_number(bank, 2) for bank in banks)


def solve_part2(banks: Sequence[str]) -> int:
    return sum(best_number(bank, 12) for bank in banks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 3.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    banks = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(banks)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(banks)}")


if __name__ == "__main__":
    main()
