from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence


Register = List[int]
Instruction = tuple[int, int, int, int]


@dataclass(frozen=True)
class Sample:
    before: tuple[int, int, int, int]
    instruction: Instruction
    after: tuple[int, int, int, int]


@dataclass(frozen=True)
class PuzzleInput:
    samples: tuple[Sample, ...]
    program: tuple[Instruction, ...]


def parse(raw: str) -> PuzzleInput:
    samples_raw, program_raw = raw.strip().split("\n\n\n\n", 1)
    sample_blocks = [block for block in samples_raw.split("\n\n") if block.strip()]

    samples: list[Sample] = []
    for block in sample_blocks:
        before_line, instruction_line, after_line = block.splitlines()
        before = tuple(int(value) for value in before_line[9:-1].split(", "))
        instruction = tuple(int(value) for value in instruction_line.split())
        after = tuple(int(value) for value in after_line[9:-1].split(", "))
        samples.append(Sample(before=before, instruction=instruction, after=after))

    program: list[Instruction] = []
    for line in program_raw.strip().splitlines():
        if not line:
            continue
        program.append(tuple(int(value) for value in line.split()))

    return PuzzleInput(samples=tuple(samples), program=tuple(program))


def _operate(registers: Sequence[int], a: int, b: int, c: int, value: int) -> Register:
    result = list(registers)
    result[c] = value
    return result


def addr(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] + registers[b])


def addi(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] + b)


def mulr(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] * registers[b])


def muli(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] * b)


def banr(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] & registers[b])


def bani(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] & b)


def borr(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] | registers[b])


def bori(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, registers[a] | b)


def setr(registers: Sequence[int], a: int, _b: int, c: int) -> Register:
    return _operate(registers, a, _b, c, registers[a])


def seti(registers: Sequence[int], a: int, _b: int, c: int) -> Register:
    return _operate(registers, a, _b, c, a)


def gtir(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, 1 if a > registers[b] else 0)


def gtri(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, 1 if registers[a] > b else 0)


def gtrr(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, 1 if registers[a] > registers[b] else 0)


def eqir(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, 1 if a == registers[b] else 0)


def eqri(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, 1 if registers[a] == b else 0)


def eqrr(registers: Sequence[int], a: int, b: int, c: int) -> Register:
    return _operate(registers, a, b, c, 1 if registers[a] == registers[b] else 0)


OPERATIONS: Dict[str, Callable[[Sequence[int], int, int, int], Register]] = {
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


def matching_operations(sample: Sample) -> set[str]:
    opcode, a, b, c = sample.instruction
    matches = set()
    for name, operation in OPERATIONS.items():
        result = operation(sample.before, a, b, c)
        if tuple(result) == sample.after:
            matches.add(name)
    return matches


def solve_part1(puzzle: PuzzleInput) -> int:
    return sum(1 for sample in puzzle.samples if len(matching_operations(sample)) >= 3)


def deduce_opcode_mapping(puzzle: PuzzleInput) -> Dict[int, str]:
    possibilities: Dict[int, set[str]] = {
        opcode: set(OPERATIONS.keys()) for opcode in range(16)
    }
    for sample in puzzle.samples:
        opcode, _a, _b, _c = sample.instruction
        possibilities[opcode] &= matching_operations(sample)

    resolved: Dict[int, str] = {}
    changed = True
    while changed:
        changed = False
        for opcode, candidates in possibilities.items():
            if len(candidates) == 1:
                name = next(iter(candidates))
                if opcode not in resolved:
                    resolved[opcode] = name
                    changed = True
        for opcode, name in resolved.items():
            for other_opcode in possibilities:
                if other_opcode != opcode:
                    possibilities[other_opcode].discard(name)

    mapping = {
        opcode: next(iter(names))
        for opcode, names in possibilities.items()
        if len(names) == 1
    }

    used_opcodes = {instruction[0] for instruction in puzzle.program}
    unresolved_in_use = used_opcodes - mapping.keys()
    if unresolved_in_use:
        raise RuntimeError(f"Unresolved opcodes: {sorted(unresolved_in_use)}")

    return mapping


def execute_program(
    program: Sequence[Instruction], mapping: Dict[int, str]
) -> Register:
    registers = [0, 0, 0, 0]
    for opcode, a, b, c in program:
        operation = OPERATIONS[mapping[opcode]]
        registers = operation(registers, a, b, c)
    return registers


def solve_part2(puzzle: PuzzleInput) -> int:
    mapping = deduce_opcode_mapping(puzzle)
    registers = execute_program(puzzle.program, mapping)
    return registers[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 16.")
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
