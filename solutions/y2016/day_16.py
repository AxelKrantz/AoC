from __future__ import annotations

import argparse
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def dragon_curve(data: str) -> str:
    inverse = "".join("1" if char == "0" else "0" for char in reversed(data))
    return f"{data}0{inverse}"


def fill_disk(state: str, length: int) -> str:
    data = state
    while len(data) < length:
        data = dragon_curve(data)
    return data[:length]


def checksum(data: str) -> str:
    result = data
    while len(result) % 2 == 0:
        pairs = ["1" if result[i] == result[i + 1] else "0" for i in range(0, len(result), 2)]
        result = "".join(pairs)
    return result


def solve(state: str, length: int) -> str:
    filled = fill_disk(state, length)
    return checksum(filled)


def solve_part1(state: str) -> str:
    return solve(state, 272)


def solve_part2(state: str) -> str:
    return solve(state, 35651584)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 16.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--length1", type=int, default=272)
    parser.add_argument("--length2", type=int, default=35651584)
    args = parser.parse_args()

    state = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve(state, args.length1)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve(state, args.length2)}")


if __name__ == "__main__":
    main()
