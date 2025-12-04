from __future__ import annotations

import argparse
from pathlib import Path
from string import ascii_lowercase


def parse(raw: str) -> str:
    return raw.strip()


def reacts(unit1: str, unit2: str) -> bool:
    return unit1 != unit2 and unit1.lower() == unit2.lower()


def reduce_polymer(polymer: str) -> str:
    stack: list[str] = []
    for unit in polymer:
        if stack and reacts(stack[-1], unit):
            stack.pop()
        else:
            stack.append(unit)
    return "".join(stack)


def solve_part1(polymer: str) -> int:
    return len(reduce_polymer(polymer))


def solve_part2(polymer: str) -> int:
    best = len(polymer)
    for letter in ascii_lowercase:
        stripped = (unit for unit in polymer if unit.lower() != letter)
        reduced = reduce_polymer("".join(stripped))
        best = min(best, len(reduced))
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 5.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    data = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
