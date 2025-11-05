from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


Pattern = Tuple[str, ...]


def parse(raw: str) -> Dict[Pattern, Pattern]:
    rules: dict[Pattern, Pattern] = {}
    for line in raw.strip().splitlines():
        left, right = line.split(" => ")
        input_pattern = tuple(left.split("/"))
        output_pattern = tuple(right.split("/"))
        for variant in variants(input_pattern):
            rules[variant] = output_pattern
    return rules


def rotate(pattern: Pattern) -> Pattern:
    size = len(pattern)
    return tuple("".join(pattern[size - j - 1][i] for j in range(size)) for i in range(size))


def flip(pattern: Pattern) -> Pattern:
    return tuple(row[::-1] for row in pattern)


def variants(pattern: Pattern) -> Iterable[Pattern]:
    current = pattern
    for _ in range(4):
        yield current
        yield flip(current)
        current = rotate(current)


def enhance(grid: Pattern, rules: Dict[Pattern, Pattern]) -> Pattern:
    size = len(grid)
    if size % 2 == 0:
        block_size = 2
    elif size % 3 == 0:
        block_size = 3
    else:
        raise ValueError("Unsupported grid size")
    blocks_per_row = size // block_size
    new_blocks: list[list[Pattern]] = []
    for by in range(blocks_per_row):
        row_blocks: list[Pattern] = []
        for bx in range(blocks_per_row):
            block = tuple(
                grid[by * block_size + dy][bx * block_size : bx * block_size + block_size]
                for dy in range(block_size)
            )
            row_blocks.append(rules[block])
        new_blocks.append(row_blocks)

    new_block_size = len(new_blocks[0][0])
    new_rows: list[str] = []
    for row_blocks in new_blocks:
        for inner_row in range(new_block_size):
            new_rows.append("".join(block[inner_row] for block in row_blocks))
    return tuple(new_rows)


def iterate(rules: Dict[Pattern, Pattern], iterations: int) -> Pattern:
    grid: Pattern = (".#.", "..#", "###")
    for _ in range(iterations):
        grid = enhance(grid, rules)
    return grid


def solve_part1(rules: Dict[Pattern, Pattern], iterations: int = 5) -> int:
    grid = iterate(rules, iterations)
    return sum(row.count("#") for row in grid)


def solve_part2(rules: Dict[Pattern, Pattern]) -> int:
    grid = iterate(rules, 18)
    return sum(row.count("#") for row in grid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 21.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--iterations", type=int, default=5)
    args = parser.parse_args()

    rules = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(rules, iterations=args.iterations)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(rules)}")


if __name__ == "__main__":
    main()
