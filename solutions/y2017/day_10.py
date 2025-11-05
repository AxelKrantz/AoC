from __future__ import annotations

import argparse
from functools import reduce
from operator import xor
from pathlib import Path
from typing import Iterable, List


def parse(raw: str) -> list[int]:
    return [int(value) for value in raw.strip().split(",") if value.strip()]


def knot_round(lengths: Iterable[int], size: int = 256, rounds: int = 1) -> List[int]:
    numbers = list(range(size))
    position = 0
    skip = 0
    numbers_len = len(numbers)
    for _ in range(rounds):
        for length in lengths:
            if length > numbers_len:
                continue
            indexes = [(position + i) % numbers_len for i in range(length)]
            values = [numbers[i] for i in indexes][::-1]
            for idx, value in zip(indexes, values):
                numbers[idx] = value
            position = (position + length + skip) % numbers_len
            skip += 1
    return numbers


def dense_hash(sparse: List[int]) -> List[int]:
    return [
        reduce(xor, sparse[i : i + 16])
        for i in range(0, len(sparse), 16)
    ]


def knot_hash(data: str) -> str:
    lengths = [ord(char) for char in data] + [17, 31, 73, 47, 23]
    sparse = knot_round(lengths, rounds=64)
    return "".join(f"{value:02x}" for value in dense_hash(sparse))


def solve_part1(lengths: list[int], size: int = 256) -> int:
    numbers = knot_round(lengths, size=size)
    return numbers[0] * numbers[1]


def solve_part2(_: list[int], raw: str | None = None) -> str:
    if raw is None:
        raise ValueError("Raw input required for part 2.")
    return knot_hash(raw.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 10.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    lengths = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(lengths)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(lengths, raw=raw)}")


if __name__ == "__main__":
    main()
