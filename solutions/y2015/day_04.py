from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def find_lowest_with_prefix(secret: str, prefix: str) -> int:
    index = 1
    while True:
        digest = hashlib.md5(f"{secret}{index}".encode("utf-8")).hexdigest()
        if digest.startswith(prefix):
            return index
        index += 1


def solve_part1(secret: str) -> int:
    return find_lowest_with_prefix(secret, "00000")


def solve_part2(secret: str) -> int:
    return find_lowest_with_prefix(secret, "000000")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 4.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    secret = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(secret)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(secret)}")


if __name__ == "__main__":
    main()
