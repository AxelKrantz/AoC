from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

Instruction = tuple[str, int, int, int]
Program = tuple[Instruction, ...]


def parse(raw: str) -> tuple[int, Program]:
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    ip_bind = int(lines[0].split()[1])
    instructions: list[Instruction] = []
    for line in lines[1:]:
        opcode, a, b, c = line.split()
        instructions.append((opcode, int(a), int(b), int(c)))
    return ip_bind, tuple(instructions)


Registers = List[int]


def operate(registers: Registers, c: int, value: int) -> Registers:
    new_registers = registers[:]
    new_registers[c] = value
    return new_registers


def addr(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] + registers[b])


def addi(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] + b)


def mulr(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] * registers[b])


def muli(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] * b)


def banr(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] & registers[b])


def bani(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] & b)


def borr(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] | registers[b])


def bori(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, registers[a] | b)


def setr(registers: Registers, a: int, _b: int, c: int) -> Registers:
    return operate(registers, c, registers[a])


def seti(registers: Registers, a: int, _b: int, c: int) -> Registers:
    return operate(registers, c, a)


def gtir(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, 1 if a > registers[b] else 0)


def gtri(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, 1 if registers[a] > b else 0)


def gtrr(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, 1 if registers[a] > registers[b] else 0)


def eqir(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, 1 if a == registers[b] else 0)


def eqri(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, 1 if registers[a] == b else 0)


def eqrr(registers: Registers, a: int, b: int, c: int) -> Registers:
    return operate(registers, c, 1 if registers[a] == registers[b] else 0)


OPERATIONS: Dict[str, Callable[[Registers, int, int, int], Registers]] = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}


def run_program(
    ip_bind: int,
    instructions: Program,
    initial_registers: Sequence[int],
    *,
    step_limit: int | None = None,
) -> Registers:
    registers = list(initial_registers)
    ip = 0
    steps = 0
    while 0 <= ip < len(instructions):
        registers[ip_bind] = ip
        opcode, a, b, c = instructions[ip]
        registers = OPERATIONS[opcode](registers, a, b, c)
        ip = registers[ip_bind] + 1
        steps += 1
        if step_limit is not None and steps >= step_limit:
            break
    return registers


def solve_part1(data: tuple[int, Program]) -> int:
    ip_bind, instructions = data
    registers = run_program(ip_bind, instructions, [0, 0, 0, 0, 0, 0])
    return registers[0]


def sum_of_divisors(number: int) -> int:
    total = 0
    limit = int(number ** 0.5)
    for value in range(1, limit + 1):
        if number % value == 0:
            total += value
            partner = number // value
            if partner != value:
                total += partner
    return total


def solve_part2(data: tuple[int, Program]) -> int:
    ip_bind, instructions = data
    registers = [0, 0, 0, 0, 0, 0]
    registers[0] = 1
    ip = 0
    target = None
    seen = 0
    while 0 <= ip < len(instructions):
        registers[ip_bind] = ip
        opcode, a, b, c = instructions[ip]
        registers = OPERATIONS[opcode](registers, a, b, c)
        ip = registers[ip_bind] + 1
        seen += 1
        if ip == 1:
            target = max(registers)
            break
        if seen > 10_000:
            raise RuntimeError("Unable to determine target value for divisor sum.")

    if target is None:
        raise RuntimeError("Target value not detected during simulation.")
    return sum_of_divisors(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 19.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    data = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
