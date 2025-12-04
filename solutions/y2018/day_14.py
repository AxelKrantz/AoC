from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def solve_part1(raw: str) -> str:
    after = int(raw)
    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(scores) < after + 10:
        total = scores[elf1] + scores[elf2]
        for digit in str(total):
            scores.append(int(digit))
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)
    return "".join(str(score) for score in scores[after : after + 10])


def solve_part2(raw: str) -> int:
    target = [int(ch) for ch in raw]
    target_len = len(target)
    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    while True:
        total = scores[elf1] + scores[elf2]
        for digit in str(total):
            scores.append(int(digit))
            if scores[-target_len:] == target:
                return len(scores) - target_len
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 14.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(raw)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(raw)}")


if __name__ == "__main__":
    main()

