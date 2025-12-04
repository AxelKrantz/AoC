from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence, Tuple


def parse(raw: str) -> list[int]:
    return [int(token) for token in raw.strip().split()]


def parse_node(numbers: Sequence[int], index: int = 0) -> tuple[int, int, int]:
    child_count = numbers[index]
    metadata_count = numbers[index + 1]
    index += 2

    metadata_sum = 0
    child_values: list[int] = []

    for _ in range(child_count):
        child_value, child_meta, index = parse_node(numbers, index)
        child_values.append(child_value)
        metadata_sum += child_meta

    metadata = numbers[index : index + metadata_count]
    index += metadata_count
    metadata_sum += sum(metadata)

    if child_count == 0:
        node_value = sum(metadata)
    else:
        node_value = sum(
            child_values[i - 1] for i in metadata if 1 <= i <= len(child_values)
        )

    return node_value, metadata_sum, index


def solve_part1(numbers: Sequence[int]) -> int:
    _, metadata_sum, _ = parse_node(numbers)
    return metadata_sum


def solve_part2(numbers: Sequence[int]) -> int:
    node_value, _, _ = parse_node(numbers)
    return node_value


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 8.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    numbers = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(numbers)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(numbers)}")


if __name__ == "__main__":
    main()
