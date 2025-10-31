from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


@dataclass
class MachineState:
    a: int
    b: int
    c: int


def parse(raw: str) -> tuple[MachineState, tuple[int, ...]]:
    sections = raw.strip().split("\n\n")
    registers: dict[str, int] = {}
    for line in sections[0].splitlines():
        name, value = line.split(":")
        registers[name.strip().split()[-1]] = int(value.strip())
    program_part = sections[1].split(":", 1)[1]
    program = tuple(int(value) for value in program_part.strip().split(","))
    state = MachineState(
        a=registers.get("A", 0),
        b=registers.get("B", 0),
        c=registers.get("C", 0),
    )
    return state, program


def combo_value(operand: int, state: MachineState) -> int:
    if operand <= 3:
        return operand
    if operand == 4:
        return state.a
    if operand == 5:
        return state.b
    if operand == 6:
        return state.c
    raise ValueError("Combo operand 7 is reserved and should not appear.")


def run_program(initial: MachineState, program: Sequence[int]) -> list[int]:
    state = MachineState(initial.a, initial.b, initial.c)
    ip = 0
    outputs: list[int] = []
    program_length = len(program)

    while ip < program_length:
        opcode = program[ip]
        operand = program[ip + 1] if ip + 1 < program_length else 0

        if opcode == 0:  # adv
            denominator = 1 << combo_value(operand, state)
            state.a //= denominator
            ip += 2
        elif opcode == 1:  # bxl
            state.b ^= operand
            ip += 2
        elif opcode == 2:  # bst
            state.b = combo_value(operand, state) % 8
            ip += 2
        elif opcode == 3:  # jnz
            if state.a != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            state.b ^= state.c
            ip += 2
        elif opcode == 5:  # out
            outputs.append(combo_value(operand, state) % 8)
            ip += 2
        elif opcode == 6:  # bdv
            denominator = 1 << combo_value(operand, state)
            state.b = state.a // denominator
            ip += 2
        elif opcode == 7:  # cdv
            denominator = 1 << combo_value(operand, state)
            state.c = state.a // denominator
            ip += 2
        else:
            raise ValueError(f"Unknown opcode {opcode}")

    return outputs


def solve_part1(initial: MachineState, program: Sequence[int]) -> str:
    outputs = run_program(initial, program)
    return ",".join(str(value) for value in outputs)


def solve_part2(initial: MachineState, program: Sequence[int]) -> int:
    target = tuple(program)

    def step(a_prev: int) -> tuple[int, int]:
        b = a_prev % 8
        b ^= 1
        c = a_prev // (1 << b)
        b ^= 5
        b ^= c
        output = b % 8
        a_next = a_prev // 8
        return output, a_next

    possible_values = {0}
    for expected in reversed(target):
        next_values: set[int] = set()
        for a_next in possible_values:
            base = a_next * 8
            for remainder in range(8):
                candidate = base + remainder
                output, resulting = step(candidate)
                if output == expected and resulting == a_next:
                    next_values.add(candidate)
        possible_values = next_values
        if not possible_values:
            break

    candidates = [
        value
        for value in possible_values
        if tuple(run_program(MachineState(value, initial.b, initial.c), program)) == target
    ]

    if not candidates:
        raise ValueError("No valid register A value found.")
    return min(candidates)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 17.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    initial, program = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(initial, program)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(initial, program)}")


if __name__ == "__main__":
    main()
