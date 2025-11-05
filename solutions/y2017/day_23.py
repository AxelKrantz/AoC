from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Instruction:
    opcode: str
    x: str
    y: str | None = None


def parse(raw: str) -> List[Instruction]:
    instructions: list[Instruction] = []
    for line in raw.strip().splitlines():
        parts = line.split()
        if not parts:
            continue
        opcode = parts[0]
        x = parts[1]
        y = parts[2] if len(parts) > 2 else None
        instructions.append(Instruction(opcode, x, y))
    return instructions


def value(operand: str, registers: Dict[str, int]) -> int:
    if operand is None:
        return 0
    if operand.lstrip("-").isdigit():
        return int(operand)
    return registers.get(operand, 0)


def execute(instructions: List[Instruction], initial_a: int = 0) -> Tuple[Dict[str, int], int]:
    registers: Dict[str, int] = {"a": initial_a}
    pointer = 0
    mul_count = 0
    while 0 <= pointer < len(instructions):
        instr = instructions[pointer]
        if instr.opcode == "set":
            registers[instr.x] = value(instr.y, registers)
        elif instr.opcode == "sub":
            registers[instr.x] = registers.get(instr.x, 0) - value(instr.y, registers)
        elif instr.opcode == "mul":
            registers[instr.x] = registers.get(instr.x, 0) * value(instr.y, registers)
            mul_count += 1
        elif instr.opcode == "jnz":
            if value(instr.x, registers) != 0:
                pointer += value(instr.y, registers)
                continue
        pointer += 1
    return registers, mul_count


def solve_part1(instructions: List[Instruction]) -> int:
    _, mul_count = execute(instructions)
    return mul_count


def is_composite(number: int) -> bool:
    if number < 2:
        return False
    if number % 2 == 0:
        return number != 2
    factor = 3
    while factor * factor <= number:
        if number % factor == 0:
            return True
        factor += 2
    return False


def solve_part2(instructions: List[Instruction]) -> int:
    b = 0
    c = 0
    for instr in instructions:
        if instr.opcode == "set" and instr.x == "b" and instr.y and instr.y.lstrip("-").isdigit():
            b = int(instr.y)
        elif instr.opcode == "mul" and instr.x == "b" and instr.y and instr.y.lstrip("-").isdigit():
            b *= int(instr.y)
        elif instr.opcode == "sub" and instr.x == "b" and instr.y and instr.y.lstrip("-").isdigit():
            b -= int(instr.y)
        elif instr.opcode == "set" and instr.x == "c" and instr.y == "b":
            c = b
        elif instr.opcode == "sub" and instr.x == "c" and instr.y and instr.y.lstrip("-").isdigit():
            c -= int(instr.y)
        elif instr.opcode == "set" and instr.x == "f":
            break

    count = 0
    for value in range(b, c + 1, 17):
        if is_composite(value):
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 23.")
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
