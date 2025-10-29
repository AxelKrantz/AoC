from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

VOWELS = set("aeiou")
FORBIDDEN = {"ab", "cd", "pq", "xy"}


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def is_nice_part1(word: str) -> bool:
    vowel_count = sum(1 for ch in word if ch in VOWELS)
    if vowel_count < 3:
        return False

    if not any(a == b for a, b in zip(word, word[1:])):
        return False

    if any(bad in word for bad in FORBIDDEN):
        return False

    return True


def has_pair_twice(word: str) -> bool:
    seen: dict[str, int] = {}
    for i in range(len(word) - 1):
        pair = word[i : i + 2]
        if pair in seen and i - seen[pair] > 1:
            return True
        if pair not in seen:
            seen[pair] = i
    return False


def has_repeat_with_gap(word: str) -> bool:
    return any(word[i] == word[i + 2] for i in range(len(word) - 2))


def is_nice_part2(word: str) -> bool:
    return has_pair_twice(word) and has_repeat_with_gap(word)


def solve_part1(words: list[str]) -> int:
    return sum(1 for word in words if is_nice_part1(word))


def solve_part2(words: list[str]) -> int:
    return sum(1 for word in words if is_nice_part2(word))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 5.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    words = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(words)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(words)}")


if __name__ == "__main__":
    main()
