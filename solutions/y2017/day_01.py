from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def captcha_sum(digits: str, step: int) -> int:
    total = 0
    length = len(digits)
    for index, char in enumerate(digits):
        if char == digits[(index + step) % length]:
            total += int(char)
    return total


def solve_part1(digits: str) -> int:
    return captcha_sum(digits, step=1)


def solve_part2(digits: str) -> int:
    return captcha_sum(digits, step=len(digits) // 2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 1.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    digits = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(digits)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(digits)}")


if __name__ == "__main__":
    main()
