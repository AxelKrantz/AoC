from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TARGET = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


@dataclass(frozen=True)
class Sue:
    index: int
    attributes: dict[str, int]


def parse(raw: str) -> list[Sue]:
    sues: list[Sue] = []
    for line in raw.strip().splitlines():
        prefix, rest = line.split(": ", 1)
        _, number = prefix.split()
        attributes: dict[str, int] = {}
        for part in rest.split(", "):
            name, value = part.split(": ")
            attributes[name] = int(value)
        sues.append(Sue(index=int(number), attributes=attributes))
    return sues


def matches_part1(sue: Sue) -> bool:
    for attribute, value in sue.attributes.items():
        if TARGET.get(attribute) != value:
            return False
    return True


def matches_part2(sue: Sue) -> bool:
    for attribute, value in sue.attributes.items():
        target = TARGET[attribute]
        if attribute in {"cats", "trees"}:
            if value <= target:
                return False
        elif attribute in {"pomeranians", "goldfish"}:
            if value >= target:
                return False
        else:
            if value != target:
                return False
    return True


def solve_part1(sues: Iterable[Sue]) -> int:
    for sue in sues:
        if matches_part1(sue):
            return sue.index
    raise ValueError("No matching Sue found for part 1.")


def solve_part2(sues: Iterable[Sue]) -> int:
    for sue in sues:
        if matches_part2(sue):
            return sue.index
    raise ValueError("No matching Sue found for part 2.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 16.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    sues = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(sues)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(sues)}")


if __name__ == "__main__":
    main()
