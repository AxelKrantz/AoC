from __future__ import annotations

import argparse
import itertools
from collections import defaultdict
from pathlib import Path


def parse(raw: str) -> dict[str, dict[str, int]]:
    table: dict[str, dict[str, int]] = defaultdict(dict)
    for line in raw.strip().splitlines():
        parts = line.rstrip(".").split()
        person = parts[0]
        sign = 1 if parts[2] == "gain" else -1
        units = sign * int(parts[3])
        neighbor = parts[-1]
        table[person][neighbor] = units
    return {person: dict(neighbors) for person, neighbors in table.items()}


def total_happiness(order: tuple[str, ...], table: dict[str, dict[str, int]]) -> int:
    total = 0
    for left, right in zip(order, order[1:]):
        total += table[left][right] + table[right][left]
    total += table[order[-1]][order[0]] + table[order[0]][order[-1]]
    return total


def maximize_happiness(table: dict[str, dict[str, int]]) -> int:
    people = list(table.keys())
    anchor = people[0]
    best = float("-inf")
    for order in itertools.permutations(people[1:]):
        seating = (anchor,) + order
        best = max(best, total_happiness(seating, table))
    return int(best)


def add_self(table: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    extended = {person: neighbors.copy() for person, neighbors in table.items()}
    extended["You"] = {}
    for person in table:
        extended[person]["You"] = 0
        extended["You"][person] = 0
    return extended


def solve_part1(table: dict[str, dict[str, int]]) -> int:
    return maximize_happiness(table)


def solve_part2(table: dict[str, dict[str, int]]) -> int:
    extended = add_self(table)
    return maximize_happiness(extended)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 13.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    table = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(table)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(table)}")


if __name__ == "__main__":
    main()
