from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, Sequence

MODULUS = 16777216


def next_secret(secret: int) -> int:
    secret = mix(secret, secret * 64)
    secret = mix(secret, secret // 32)
    secret = mix(secret, secret * 2048)
    return secret


def mix(secret: int, value: int) -> int:
    secret ^= value
    return secret % MODULUS


def generate_secret(secret: int, iterations: int) -> int:
    for _ in range(iterations):
        secret = next_secret(secret)
    return secret


def parse(raw: str) -> list[int]:
    return [int(line.strip()) for line in raw.splitlines() if line.strip()]


def price(secret: int) -> int:
    return secret % 10


def pattern_profits(initial: int, iterations: int = 2000) -> Dict[tuple[int, int, int, int], int]:
    secret = initial
    prices = [price(secret)]
    diffs: list[int] = []
    seen: Dict[tuple[int, int, int, int], int] = {}

    for _ in range(iterations):
        secret = next_secret(secret)
        current_price = price(secret)
        previous_price = prices[-1]
        prices.append(current_price)
        diffs.append(current_price - previous_price)

        if len(diffs) >= 4:
            pattern = tuple(diffs[-4:])
            if pattern not in seen:
                seen[pattern] = current_price
    return seen


def solve_part1(initial_secrets: Sequence[int]) -> int:
    total = 0
    for secret in initial_secrets:
        final_secret = generate_secret(secret, 2000)
        total += final_secret
    return total


def solve_part2(initial_secrets: Sequence[int]) -> int:
    totals: Dict[tuple[int, int, int, int], int] = defaultdict(int)
    for secret in initial_secrets:
        profits = pattern_profits(secret)
        for pattern, value in profits.items():
            totals[pattern] += value
    return max(totals.values(), default=0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 22.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    initial_secrets = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(initial_secrets)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(initial_secrets)}")


if __name__ == "__main__":
    main()
