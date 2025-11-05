from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> list[list[str]]:
    return [line.strip().split() for line in raw.strip().splitlines() if line.strip()]


def valid_passphrase(words: list[str]) -> bool:
    return len(words) == len(set(words))


def valid_passphrase_anagram(words: list[str]) -> bool:
    signatures = {"".join(sorted(word)) for word in words}
    return len(words) == len(signatures)


def solve_part1(passphrases: list[list[str]]) -> int:
    return sum(1 for words in passphrases if valid_passphrase(words))


def solve_part2(passphrases: list[list[str]]) -> int:
    return sum(1 for words in passphrases if valid_passphrase_anagram(words))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 4.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    passphrases = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(passphrases)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(passphrases)}")


if __name__ == "__main__":
    main()
