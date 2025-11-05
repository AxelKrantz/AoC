from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple


MODULUS = 2_147_483_647
FACTOR_A = 16807
FACTOR_B = 48271


def parse(raw: str) -> Tuple[int, int]:
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    seed_a = int(lines[0].split()[-1])
    seed_b = int(lines[1].split()[-1])
    return seed_a, seed_b


def generator(seed: int, factor: int, multiple: int = 1) -> Iterable[int]:
    value = seed
    while True:
        value = (value * factor) % MODULUS
        if value % multiple == 0:
            yield value


def count_matches(seed_a: int, seed_b: int, pairs: int, multiple_a: int = 1, multiple_b: int = 1) -> int:
    gen_a = generator(seed_a, FACTOR_A, multiple_a)
    gen_b = generator(seed_b, FACTOR_B, multiple_b)
    mask = 0xFFFF
    matches = 0
    for _ in range(pairs):
        if next(gen_a) & mask == next(gen_b) & mask:
            matches += 1
    return matches


def solve_part1(seeds: Tuple[int, int], pairs: int = 40_000_000) -> int:
    seed_a, seed_b = seeds
    return count_matches(seed_a, seed_b, pairs)


def solve_part2(seeds: Tuple[int, int], pairs: int = 5_000_000) -> int:
    seed_a, seed_b = seeds
    return count_matches(seed_a, seed_b, pairs, multiple_a=4, multiple_b=8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 15.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--pairs1", type=int, default=40_000_000)
    parser.add_argument("--pairs2", type=int, default=5_000_000)
    args = parser.parse_args()

    seeds = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(seeds, pairs=args.pairs1)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(seeds, pairs=args.pairs2)}")


if __name__ == "__main__":
    main()
