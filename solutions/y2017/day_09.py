from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def process(stream: str) -> tuple[int, int]:
    depth = 0
    score = 0
    garbage = False
    garbage_count = 0
    skip_next = False
    for char in stream:
        if skip_next:
            skip_next = False
            continue
        if garbage:
            if char == "!":
                skip_next = True
            elif char == ">":
                garbage = False
            else:
                garbage_count += 1
            continue
        if char == "<":
            garbage = True
        elif char == "{":
            depth += 1
            score += depth
        elif char == "}":
            depth -= 1
    return score, garbage_count


def solve_part1(stream: str) -> int:
    score, _ = process(stream)
    return score


def solve_part2(stream: str) -> int:
    _, garbage = process(stream)
    return garbage


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 9.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    stream = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(stream)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(stream)}")


if __name__ == "__main__":
    main()
