from __future__ import annotations

import argparse
import collections
from pathlib import Path
from typing import Iterable, Sequence


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.strip().splitlines() if line.strip()]


def message(columns: Sequence[str], *, least_common: bool = False) -> str:
    result: list[str] = []
    for column in columns:
        counter = collections.Counter(column)
        if least_common:
            char = min(counter.items(), key=lambda item: (item[1], item[0]))[0]
        else:
            char = min(counter.items(), key=lambda item: (-item[1], item[0]))[0]
        result.append(char)
    return "".join(result)


def solve_part1(rows: Iterable[str]) -> str:
    columns = list(zip(*rows))
    joined = ["".join(column) for column in columns]
    return message(joined)


def solve_part2(rows: Iterable[str]) -> str:
    columns = list(zip(*rows))
    joined = ["".join(column) for column in columns]
    return message(joined, least_common=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 6.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    rows = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(rows)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(rows)}")


if __name__ == "__main__":
    main()
