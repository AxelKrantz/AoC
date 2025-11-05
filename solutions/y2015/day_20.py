from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> int:
    return int(raw.strip())


def find_min_house(target: int, multiplier: int, *, delivery_limit: int | None) -> int:
    size = max(1, target // multiplier)
    while True:
        houses = [0] * (size + 1)
        for elf in range(1, size + 1):
            delivered = 0
            for house in range(elf, size + 1, elf):
                houses[house] += elf * multiplier
                delivered += 1
                if delivery_limit is not None and delivered >= delivery_limit:
                    break
        for house, presents in enumerate(houses):
            if house > 0 and presents >= target:
                return house
        size *= 2


def solve_part1(target: int) -> int:
    return find_min_house(target, 10, delivery_limit=None)


def solve_part2(target: int) -> int:
    return find_min_house(target, 11, delivery_limit=50)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 20.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    target = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(target)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(target)}")


if __name__ == "__main__":
    main()
