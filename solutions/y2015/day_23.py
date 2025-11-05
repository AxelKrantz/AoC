from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


Instruction = Tuple[str, tuple[str, ...]]


def parse(raw: str) -> List[Instruction]:
    program: list[Instruction] = []
    for line in raw.strip().splitlines():
        parts = line.replace(",", "").split()
        opcode = parts[0]
        operands = tuple(parts[1:])
        program.append((opcode, operands))
    return program


def run(program: List[Instruction], register_a: int, register_b: int) -> dict[str, int]:
    registers = {"a": register_a, "b": register_b}
    pc = 0
    while 0 <= pc < len(program):
        opcode, operands = program[pc]
        if opcode == "hlf":
            registers[operands[0]] //= 2
            pc += 1
        elif opcode == "tpl":
            registers[operands[0]] *= 3
            pc += 1
        elif opcode == "inc":
            registers[operands[0]] += 1
            pc += 1
        elif opcode == "jmp":
            pc += int(operands[0])
        elif opcode == "jie":
            register = operands[0]
            offset = int(operands[1])
            if registers[register] % 2 == 0:
                pc += offset
            else:
                pc += 1
        elif opcode == "jio":
            register = operands[0]
            offset = int(operands[1])
            if registers[register] == 1:
                pc += offset
            else:
                pc += 1
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
    return registers


def solve_part1(program: List[Instruction]) -> int:
    result = run(program, register_a=0, register_b=0)
    return result["b"]


def solve_part2(program: List[Instruction]) -> int:
    result = run(program, register_a=1, register_b=0)
    return result["b"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 23.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    program = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(program)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(program)}")


if __name__ == "__main__":
    main()
