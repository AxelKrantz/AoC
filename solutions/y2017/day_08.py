from __future__ import annotations

import argparse
from collections import defaultdict
from operator import eq, ge, gt, le, lt, ne
from pathlib import Path
from typing import Callable, Dict, Iterable, Tuple


ConditionOp = Callable[[int, int], bool]
Instruction = Tuple[str, int, str, ConditionOp, int]

OPS: dict[str, ConditionOp] = {
    ">": gt,
    "<": lt,
    ">=": ge,
    "<=": le,
    "==": eq,
    "!=": ne,
}


def parse(raw: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in raw.strip().splitlines():
        parts = line.split()
        if not parts:
            continue
        register = parts[0]
        operation = parts[1]
        amount = int(parts[2])
        condition_register = parts[4]
        condition_op = OPS[parts[5]]
        condition_value = int(parts[6])
        signed_amount = amount if operation == "inc" else -amount
        instructions.append((register, signed_amount, condition_register, condition_op, condition_value))
    return instructions


def execute(instructions: Iterable[Instruction]) -> tuple[int, int]:
    registers: Dict[str, int] = defaultdict(int)
    max_value_ever = float("-inf")
    for register, amount, cond_reg, cond_op, cond_value in instructions:
        if cond_op(registers[cond_reg], cond_value):
            registers[register] += amount
            max_value_ever = max(max_value_ever, registers[register])
    final_max = max(registers.values(), default=0)
    if max_value_ever == float("-inf"):
        max_value_ever = final_max
    return final_max, int(max_value_ever)


def solve_part1(instructions: Iterable[Instruction]) -> int:
    final, _ = execute(instructions)
    return final


def solve_part2(instructions: Iterable[Instruction]) -> int:
    _, highest = execute(instructions)
    return highest


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 8.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    instructions = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(instructions)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(instructions)}")


if __name__ == "__main__":
    main()
