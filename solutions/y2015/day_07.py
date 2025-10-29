from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
from typing import Dict, Tuple

Expression = Tuple[str, tuple[str, ...]]


def parse(raw: str) -> dict[str, Expression]:
    expressions: dict[str, Expression] = {}
    for line in raw.splitlines():
        if not line:
            continue
        formula, _, target = line.partition(" -> ")
        tokens = formula.split()
        if len(tokens) == 1:
            expressions[target] = ("VALUE", (tokens[0],))
        elif len(tokens) == 2:
            op, operand = tokens
            expressions[target] = (op.upper(), (operand,))
        elif len(tokens) == 3:
            left, op, right = tokens
            expressions[target] = (op.upper(), (left, right))
        else:
            raise ValueError(f"Unsupported instruction: {line}")
    return expressions


def is_number(token: str) -> bool:
    return token.isdigit()


def resolve(token: str, evaluator: "Evaluator") -> int:
    if is_number(token):
        return int(token)
    return evaluator.evaluate(token)


class Evaluator:
    def __init__(self, expressions: Dict[str, Expression]):
        self.expressions = expressions
        self.cache: dict[str, int] = {}

    def evaluate(self, wire: str) -> int:
        if wire in self.cache:
            return self.cache[wire]

        op, args = self.expressions[wire]
        if op == "VALUE":
            value = resolve(args[0], self)
        elif op == "NOT":
            value = (~resolve(args[0], self)) & 0xFFFF
        elif op == "AND":
            value = resolve(args[0], self) & resolve(args[1], self)
        elif op == "OR":
            value = resolve(args[0], self) | resolve(args[1], self)
        elif op == "LSHIFT":
            value = (resolve(args[0], self) << int(args[1])) & 0xFFFF
        elif op == "RSHIFT":
            value = resolve(args[0], self) >> int(args[1])
        else:
            raise ValueError(f"Unknown operation {op}")

        self.cache[wire] = value
        return value

    def override(self, wire: str, value: int) -> None:
        self.cache[wire] = value

    def clear_cache(self) -> None:
        self.cache.clear()


def solve_part1(expressions: dict[str, Expression]) -> int:
    evaluator = Evaluator(expressions)
    return evaluator.evaluate("a")


def solve_part2(expressions: dict[str, Expression]) -> int:
    evaluator = Evaluator(expressions)
    part1 = evaluator.evaluate("a")
    evaluator.clear_cache()
    evaluator.override("b", part1)
    return evaluator.evaluate("a")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 7.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    expressions = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(expressions)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(expressions)}")


if __name__ == "__main__":
    main()
