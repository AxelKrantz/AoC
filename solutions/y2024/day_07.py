from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

Equation = tuple[int, tuple[int, ...]]


def parse(raw: str) -> list[Equation]:
    equations: list[Equation] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        left, right = line.split(":")
        target = int(left.strip())
        numbers = tuple(int(value) for value in right.strip().split())
        equations.append((target, numbers))
    return equations


def can_make_value(target: int, numbers: Sequence[int], operators: Sequence[str]) -> bool:
    first, *rest = numbers

    @lru_cache(maxsize=None)
    def dfs(index: int, total: int) -> bool:
        if index == len(rest):
            return total == target
        next_value = rest[index]
        # Recurse with each available operator.
        for op in operators:
            if op == "+":
                new_total = total + next_value
            elif op == "*":
                new_total = total * next_value
            elif op == "||":
                new_total = int(f"{total}{next_value}")
            else:  # pragma: no cover - defensive
                raise ValueError(f"Unsupported operator {op!r}")

            if new_total > target:
                continue
            if dfs(index + 1, new_total):
                return True
        return False

    return dfs(0, first)


def total_calibration_result(equations: Iterable[Equation], operators: Sequence[str]) -> int:
    return sum(target for target, numbers in equations if can_make_value(target, numbers, operators))


def solve_part1(equations: Iterable[Equation]) -> int:
    return total_calibration_result(equations, operators=["+", "*"])


def solve_part2(equations: Iterable[Equation]) -> int:
    return total_calibration_result(equations, operators=["+", "*", "||"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 7.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    equations = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(equations)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(equations)}")


if __name__ == "__main__":
    main()
