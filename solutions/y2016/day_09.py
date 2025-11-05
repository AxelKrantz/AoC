from __future__ import annotations

import argparse
import re
from pathlib import Path


MARKER_RE = re.compile(r"\((\d+)x(\d+)\)")


def parse(raw: str) -> str:
    return raw.strip()


def decompress_length(data: str, recursive: bool = False) -> int:
    index = 0
    total = 0
    while index < len(data):
        if data[index] != "(":
            total += 1
            index += 1
            continue
        match = MARKER_RE.match(data, index)
        if not match:
            total += 1
            index += 1
            continue
        length, repeat = map(int, match.groups())
        index = match.end()
        segment = data[index : index + length]
        if recursive:
            total += repeat * decompress_length(segment, recursive=True)
        else:
            total += repeat * len(segment)
        index += length
    return total


def solve_part1(data: str) -> int:
    return decompress_length(data, recursive=False)


def solve_part2(data: str) -> int:
    return decompress_length(data, recursive=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 9.")
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
