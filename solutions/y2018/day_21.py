from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Dict, Generator, Sequence, Tuple

Instruction = tuple[str, int, int, int]
Registers = list[int]


def parse(raw: str) -> tuple[int, tuple[Instruction, ...]]:
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    ip_bind = int(lines[0].split()[1])
    instructions: list[Instruction] = []
    for line in lines[1:]:
        opcode, a, b, c = line.split()
        instructions.append((opcode, int(a), int(b), int(c)))
    return ip_bind, tuple(instructions)


def addr(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] + registers[b]
    return registers


def addi(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] + b
    return registers


def mulr(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] * registers[b]
    return registers


def muli(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] * b
    return registers


def banr(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] & registers[b]
    return registers


def bani(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] & b
    return registers


def borr(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] | registers[b]
    return registers


def bori(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = registers[a] | b
    return registers


def setr(registers: Registers, a: int, _b: int, c: int) -> Registers:
    registers[c] = registers[a]
    return registers


def seti(registers: Registers, a: int, _b: int, c: int) -> Registers:
    registers[c] = a
    return registers


def gtir(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = 1 if a > registers[b] else 0
    return registers


def gtri(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = 1 if registers[a] > b else 0
    return registers


def gtrr(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = 1 if registers[a] > registers[b] else 0
    return registers


def eqir(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = 1 if a == registers[b] else 0
    return registers


def eqri(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = 1 if registers[a] == b else 0
    return registers


def eqrr(registers: Registers, a: int, b: int, c: int) -> Registers:
    registers[c] = 1 if registers[a] == registers[b] else 0
    return registers


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


def find_comparison(instructions: Sequence[Instruction]) -> tuple[int, int]:
    for index, (opcode, a, b, _c) in enumerate(instructions):
        if opcode == "eqrr" and (a == 0 or b == 0):
            compare_reg = b if a == 0 else a
            return index, compare_reg
    raise RuntimeError("Unable to locate eqrr instruction comparing against register 0.")


def is_optimized_program(instructions: Sequence[Instruction]) -> bool:
    if len(instructions) < 30:
        return False
    patterns = [
        ("bori", 2, 65536, 5),
        ("seti", 5234604, 6, 2),
        ("bani", 5, 255, 3),
        ("addr", 2, 3, 2),
        ("bani", 2, 16777215, 2),
        ("muli", 2, 65899, 2),
        ("bani", 2, 16777215, 2),
        ("gtir", 256, 5, 3),
        ("seti", 27, 2, 4),
        ("seti", 0, 0, 3),
    ]
    for offset, pattern in enumerate(patterns, start=7):
        opcode, a, b, c = pattern
        inst = instructions[offset]
        if inst[0] != opcode or inst[1] != a or inst[2] != b or inst[3] != c:
            return False
    return True


_OPTIMIZED_CACHE: tuple[int, int] | None = None


def compute_optimized_results() -> tuple[int, int]:
    global _OPTIMIZED_CACHE
    if _OPTIMIZED_CACHE is not None:
        return _OPTIMIZED_CACHE

    seen: set[int] = set()
    first_value: int | None = None
    last_unique = 0
    register2 = 0

    while True:
        register5 = register2 | 65536
        register2 = 5234604
        while True:
            register2 = (register2 + (register5 & 255)) & 16777215
            register2 = (register2 * 65899) & 16777215
            if register5 < 256:
                if first_value is None:
                    first_value = register2
                if register2 in seen:
                    _OPTIMIZED_CACHE = (first_value, last_unique)
                    return _OPTIMIZED_CACHE
                seen.add(register2)
                last_unique = register2
                break
            register5 //= 256


def value_sequence(
    ip_bind: int, instructions: Sequence[Instruction]
) -> Generator[int, None, None]:
    check_ip, compare_reg = find_comparison(instructions)
    registers: Registers = [0, 0, 0, 0, 0, 0]
    ip = 0
    while 0 <= ip < len(instructions):
        if ip == check_ip:
            yield registers[compare_reg]
        registers[ip_bind] = ip
        opcode, a, b, c = instructions[ip]
        registers = OPERATIONS[opcode](registers, a, b, c)
        ip = registers[ip_bind] + 1


def solve_part1(data: tuple[int, tuple[Instruction, ...]]) -> int:
    ip_bind, instructions = data
    if is_optimized_program(instructions):
        first_value, _ = compute_optimized_results()
        return first_value
    sequence = value_sequence(ip_bind, instructions)
    return next(sequence)


def solve_part2(data: tuple[int, tuple[Instruction, ...]]) -> int:
    ip_bind, instructions = data
    if is_optimized_program(instructions):
        _, last_value = compute_optimized_results()
        return last_value
    sequence = value_sequence(ip_bind, instructions)
    seen = set()
    last_value = 0
    for value in sequence:
        if value in seen:
            return last_value
        seen.add(value)
        last_value = value
    raise RuntimeError("Sequence terminated without repeating values.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 21.")
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
