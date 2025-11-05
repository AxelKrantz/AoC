from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple


@dataclass(frozen=True)
class Action:
    write: int
    move: int
    next_state: str


Blueprint = Tuple[str, int, Dict[str, Dict[int, Action]]]


BEGIN_RE = re.compile(r"Begin in state (\w).")
STEPS_RE = re.compile(r"Perform a diagnostic checksum after (\d+) steps.")
STATE_RE = re.compile(r"In state (\w):")
VALUE_RE = re.compile(r"If the current value is (\d):")
WRITE_RE = re.compile(r"- Write the value (\d).")
MOVE_RE = re.compile(r"- Move one slot to the (left|right).")
NEXT_RE = re.compile(r"- Continue with state (\w).")


def parse(raw: str) -> Blueprint:
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    begin_state = BEGIN_RE.match(lines[0]).group(1)
    steps = int(STEPS_RE.match(lines[1]).group(1))
    rules: Dict[str, Dict[int, Action]] = {}
    index = 2
    while index < len(lines):
        state = STATE_RE.match(lines[index]).group(1)
        index += 1
        rules[state] = {}
        for _ in range(2):
            value = int(VALUE_RE.match(lines[index]).group(1))
            write = int(WRITE_RE.match(lines[index + 1]).group(1))
            move = -1 if MOVE_RE.match(lines[index + 2]).group(1) == "left" else 1
            next_state = NEXT_RE.match(lines[index + 3]).group(1)
            rules[state][value] = Action(write, move, next_state)
            index += 4
    return begin_state, steps, rules


def run_machine(blueprint: Blueprint) -> int:
    state, steps, rules = blueprint
    tape: Dict[int, int] = {}
    position = 0
    for _ in range(steps):
        value = tape.get(position, 0)
        action = rules[state][value]
        if action.write == 0:
            tape.pop(position, None)
        else:
            tape[position] = action.write
        position += action.move
        state = action.next_state
    return len(tape)


def solve_part1(blueprint: Blueprint) -> int:
    return run_machine(blueprint)


def solve_part2(blueprint: Blueprint) -> int:
    return run_machine(blueprint)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 25.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    blueprint = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(blueprint)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(blueprint)}")


if __name__ == "__main__":
    main()
