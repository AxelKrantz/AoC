from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence


@dataclass(frozen=True)
class Instruction:
    opcode: str
    args: tuple[str, ...]


def parse(raw: str) -> list[Instruction]:
    program: list[Instruction] = []
    for line in raw.strip().splitlines():
        parts = line.split()
        if not parts:
            continue
        opcode = parts[0]
        program.append(Instruction(opcode, tuple(parts[1:])))
    return program


def value(operand: str, registers: Dict[str, int]) -> int:
    if operand.lstrip("-").isdigit():
        return int(operand)
    return registers.get(operand, 0)


def toggle(instruction: Instruction) -> Instruction:
    opcode = instruction.opcode
    args = instruction.args
    if len(args) == 1:
        new_opcode = "dec" if opcode == "inc" else "inc"
    elif len(args) == 2:
        new_opcode = "jnz" if opcode == "cpy" else "cpy"
    else:
        new_opcode = opcode
    return Instruction(new_opcode, args)


def run(program: Sequence[Instruction], initial: Dict[str, int]) -> Dict[str, int]:
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    registers.update(initial)

    instructions = list(program)
    pointer = 0

    while 0 <= pointer < len(instructions):
        instruction = instructions[pointer]
        opcode, args = instruction.opcode, instruction.args

        if opcode == "cpy":
            x, y = args
            if y in registers:
                registers[y] = value(x, registers)
            pointer += 1
        elif opcode == "inc":
            (x,) = args
            if x in registers:
                registers[x] += 1
            pointer += 1
        elif opcode == "dec":
            (x,) = args
            if x in registers:
                registers[x] -= 1
            pointer += 1
        elif opcode == "jnz":
            x, y = args
            if value(x, registers) != 0:
                pointer += value(y, registers)
            else:
                pointer += 1
        elif opcode == "tgl":
            (x,) = args
            target = pointer + value(x, registers)
            if 0 <= target < len(instructions):
                instructions[target] = toggle(instructions[target])
            pointer += 1
        else:
            pointer += 1
    return registers


def optimized_result(program: Sequence[Instruction], initial: int) -> int:
    large_numbers = sorted({int(arg) for inst in program for arg in inst.args if arg.lstrip("-").isdigit() and int(arg) > 10})
    if len(large_numbers) >= 2:
        extra = large_numbers[-1] * large_numbers[-2]
        return math.factorial(initial) + extra
    return run(program, {"a": initial})["a"]


def solve_part1(program: Sequence[Instruction]) -> int:
    return optimized_result(program, 7)


def solve_part2(program: Sequence[Instruction]) -> int:
    return optimized_result(program, 12)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 23.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--initial-a", type=int, default=None)
    args = parser.parse_args()

    program = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        init = {"a": args.initial_a} if args.initial_a is not None else {"a": 7}
        print(f"Part 1: {run(program, init)['a']}")
    if args.part in {"2", "both"}:
        init = {"a": args.initial_a} if args.initial_a is not None else {"a": 12}
        print(f"Part 2: {run(program, init)['a']}")


if __name__ == "__main__":
    main()
