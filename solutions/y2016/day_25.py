from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Sequence


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
        program.append(Instruction(parts[0], tuple(parts[1:])))
    return program


def value(operand: str, registers: Dict[str, int]) -> int:
    if operand.lstrip("-").isdigit():
        return int(operand)
    return registers.get(operand, 0)


def is_clock_signal(program: Sequence[Instruction], initial_a: int, required: int = 100) -> bool:
    registers = {"a": initial_a, "b": 0, "c": 0, "d": 0}
    ip = 0
    expected = 0
    produced = 0
    steps = 0
    max_steps = 1_000_000

    while 0 <= ip < len(program) and steps < max_steps:
        opcode, args = program[ip].opcode, program[ip].args
        steps += 1

        if opcode == "cpy":
            x, y = args
            if y in registers:
                registers[y] = value(x, registers)
            ip += 1
        elif opcode == "inc":
            (x,) = args
            if x in registers:
                registers[x] += 1
            ip += 1
        elif opcode == "dec":
            (x,) = args
            if x in registers:
                registers[x] -= 1
            ip += 1
        elif opcode == "jnz":
            x, y = args
            if value(x, registers) != 0:
                ip += value(y, registers)
            else:
                ip += 1
        elif opcode == "out":
            (x,) = args
            signal = value(x, registers)
            if signal not in (0, 1) or signal != expected:
                return False
            expected ^= 1
            produced += 1
            if produced >= required:
                return True
            ip += 1
        else:
            ip += 1
    return False


def solve_part1(program: Sequence[Instruction]) -> int:
    a = 0
    while True:
        if is_clock_signal(program, a):
            return a
        a += 1


def solve_part2(program: Sequence[Instruction]) -> int:
    return solve_part1(program)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 25.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    program = parse(args.input_path.read_text(encoding="utf-8"))

    result = solve_part1(program)
    print(f"Part 1: {result}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
