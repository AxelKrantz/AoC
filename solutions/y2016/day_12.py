from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence


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
        if opcode in {"cpy", "jnz"}:
            instructions.append(Instruction(opcode, parts[1], parts[2]))
        else:
            instructions.append(Instruction(opcode, parts[1]))
    return instructions


def value(operand: str, registers: Dict[str, int]) -> int:
    if operand.lstrip("-").isdigit():
        return int(operand)
    return registers.get(operand, 0)


def run(instructions: Sequence[Instruction], initial: Dict[str, int] | None = None) -> Dict[str, int]:
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    if initial:
        registers.update(initial)
    pointer = 0
    while 0 <= pointer < len(instructions):
        instr = instructions[pointer]
        if instr.opcode == "cpy":
            if instr.y and instr.y in registers:
                registers[instr.y] = value(instr.x, registers)
            pointer += 1
        elif instr.opcode == "inc":
            registers[instr.x] += 1
            pointer += 1
        elif instr.opcode == "dec":
            registers[instr.x] -= 1
            pointer += 1
        elif instr.opcode == "jnz":
            offset = value(instr.y or "0", registers)
            if value(instr.x, registers) != 0:
                pointer += offset
            else:
                pointer += 1
        else:
            raise ValueError(f"Unknown opcode: {instr.opcode}")
    return registers


def solve_part1(instructions: Sequence[Instruction]) -> int:
    registers = run(instructions)
    return registers["a"]


def solve_part2(instructions: Sequence[Instruction]) -> int:
    registers = run(instructions, {"c": 1})
    return registers["a"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 12.")
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
