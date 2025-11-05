from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Deque, Dict, List, Optional, Tuple


Instruction = Tuple[str, Tuple[str, ...]]


def parse(raw: str) -> List[Instruction]:
    instructions: list[Instruction] = []
    for line in raw.strip().splitlines():
        parts = tuple(line.split())
        instructions.append((parts[0], parts[1:]))
    return instructions


def value(operand: str, registers: Dict[str, int]) -> int:
    if operand.lstrip("-").isdigit():
        return int(operand)
    return registers.get(operand, 0)


def solve_part1(instructions: List[Instruction]) -> int:
    registers: Dict[str, int] = {}
    last_sound = 0
    pointer = 0
    while 0 <= pointer < len(instructions):
        opcode, args = instructions[pointer]
        if opcode == "snd":
            last_sound = value(args[0], registers)
        elif opcode == "set":
            registers[args[0]] = value(args[1], registers)
        elif opcode == "add":
            registers[args[0]] = registers.get(args[0], 0) + value(args[1], registers)
        elif opcode == "mul":
            registers[args[0]] = registers.get(args[0], 0) * value(args[1], registers)
        elif opcode == "mod":
            registers[args[0]] = registers.get(args[0], 0) % value(args[1], registers)
        elif opcode == "rcv":
            if value(args[0], registers) != 0:
                return last_sound
        elif opcode == "jgz":
            if value(args[0], registers) > 0:
                pointer += value(args[1], registers)
                continue
        pointer += 1
    raise ValueError("No recover executed")


class Program:
    def __init__(self, pid: int, instructions: List[Instruction]) -> None:
        self.pid = pid
        self.instructions = instructions
        self.registers: Dict[str, int] = {"p": pid}
        self.pointer = 0
        self.queue: Deque[int] = deque()
        self.sent = 0
        self.blocked = False

    def step(self, other_queue: Deque[int]) -> Optional[bool]:
        if not (0 <= self.pointer < len(self.instructions)):
            self.blocked = True
            return None
        opcode, args = self.instructions[self.pointer]
        if opcode == "snd":
            value_to_send = value(args[0], self.registers)
            other_queue.append(value_to_send)
            self.sent += 1
            self.pointer += 1
            self.blocked = False
        elif opcode == "set":
            self.registers[args[0]] = value(args[1], self.registers)
            self.pointer += 1
        elif opcode == "add":
            self.registers[args[0]] = self.registers.get(args[0], 0) + value(args[1], self.registers)
            self.pointer += 1
        elif opcode == "mul":
            self.registers[args[0]] = self.registers.get(args[0], 0) * value(args[1], self.registers)
            self.pointer += 1
        elif opcode == "mod":
            self.registers[args[0]] = self.registers.get(args[0], 0) % value(args[1], self.registers)
            self.pointer += 1
        elif opcode == "rcv":
            if self.queue:
                self.registers[args[0]] = self.queue.popleft()
                self.pointer += 1
                self.blocked = False
            else:
                self.blocked = True
                return False
        elif opcode == "jgz":
            if value(args[0], self.registers) > 0:
                self.pointer += value(args[1], self.registers)
            else:
                self.pointer += 1
        else:
            self.pointer += 1
        return True


def solve_part2(instructions: List[Instruction]) -> int:
    program0 = Program(0, instructions)
    program1 = Program(1, instructions)
    while True:
        progressed0 = program0.step(program1.queue)
        progressed1 = program1.step(program0.queue)
        if (progressed0 is False or progressed0 is None) and (progressed1 is False or progressed1 is None):
            if (program0.blocked and not program0.queue) and (program1.blocked and not program1.queue):
                break
        if progressed0 is None and progressed1 is None:
            break
    return program1.sent


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 18.")
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
