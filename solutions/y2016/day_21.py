from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Operation:
    type: str
    args: tuple[str, ...]


SWAP_POS_RE = re.compile(r"swap position (\d+) with position (\d+)")
SWAP_LET_RE = re.compile(r"swap letter (\w) with letter (\w)")
ROTATE_RE = re.compile(r"rotate (left|right) (\d+) step")
ROTATE_POS_RE = re.compile(r"rotate based on position of letter (\w)")
REVERSE_RE = re.compile(r"reverse positions (\d+) through (\d+)")
MOVE_RE = re.compile(r"move position (\d+) to position (\d+)")


def parse(raw: str) -> list[Operation]:
    operations: list[Operation] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if match := SWAP_POS_RE.match(line):
            operations.append(Operation("swap_pos", match.groups()))
        elif match := SWAP_LET_RE.match(line):
            operations.append(Operation("swap_letter", match.groups()))
        elif match := ROTATE_RE.match(line):
            direction, steps = match.groups()
            operations.append(Operation("rotate", (direction, steps)))
        elif match := ROTATE_POS_RE.match(line):
            (letter,) = match.groups()
            operations.append(Operation("rotate_pos", (letter,)))
        elif match := REVERSE_RE.match(line):
            operations.append(Operation("reverse", match.groups()))
        elif match := MOVE_RE.match(line):
            operations.append(Operation("move", match.groups()))
        else:
            raise ValueError(f"Unknown instruction: {line}")
    return operations


def rotate(s: List[str], steps: int) -> List[str]:
    steps %= len(s)
    return s[-steps:] + s[:-steps]


def apply(operation: Operation, password: List[str]) -> List[str]:
    result = password[:]
    if operation.type == "swap_pos":
        x, y = map(int, operation.args)
        result[x], result[y] = result[y], result[x]
    elif operation.type == "swap_letter":
        a, b = operation.args
        result = [b if char == a else a if char == b else char for char in result]
    elif operation.type == "rotate":
        direction, steps = operation.args
        steps_int = int(steps)
        if direction == "left":
            steps_int = -steps_int
        result = rotate(result, steps_int)
    elif operation.type == "rotate_pos":
        (letter,) = operation.args
        index = result.index(letter)
        steps = 1 + index
        if index >= 4:
            steps += 1
        result = rotate(result, steps)
    elif operation.type == "reverse":
        x, y = map(int, operation.args)
        if x > y:
            x, y = y, x
        result = result[:x] + list(reversed(result[x : y + 1])) + result[y + 1 :]
    elif operation.type == "move":
        x, y = map(int, operation.args)
        char = result.pop(x)
        result.insert(y, char)
    else:
        raise ValueError(f"Unsupported operation: {operation.type}")
    return result


def apply_inverse(operation: Operation, password: List[str]) -> List[str]:
    result = password[:]
    if operation.type == "swap_pos":
        return apply(operation, result)
    if operation.type == "swap_letter":
        return apply(operation, result)
    if operation.type == "rotate":
        direction, steps = operation.args
        inverse_direction = "left" if direction == "right" else "right"
        inverse_operation = Operation("rotate", (inverse_direction, steps))
        return apply(inverse_operation, result)
    if operation.type == "rotate_pos":
        (letter,) = operation.args
        for shift in range(len(result)):
            candidate = rotate(result, -shift)
            if apply(operation, candidate) == result:
                return candidate
        raise ValueError("Unable to invert rotate_pos operation.")
    if operation.type == "reverse":
        return apply(operation, result)
    if operation.type == "move":
        x, y = operation.args
        inverse_operation = Operation("move", (y, x))
        return apply(inverse_operation, result)
    raise ValueError(f"Unsupported operation: {operation.type}")


def scramble(password: str, operations: Iterable[Operation]) -> str:
    chars = list(password)
    for op in operations:
        chars = apply(op, chars)
    return "".join(chars)


def unscramble(password: str, operations: Iterable[Operation]) -> str:
    chars = list(password)
    for operation in reversed(list(operations)):
        chars = apply_inverse(operation, chars)
    return "".join(chars)


def solve_part1(operations: Iterable[Operation], starting: str = "abcdefgh") -> str:
    return scramble(starting, operations)


def solve_part2(operations: Iterable[Operation], scrambled: str = "fbgdceah") -> str:
    return unscramble(scrambled, operations)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 21.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--password", default="abcdefgh")
    parser.add_argument("--scrambled", default="fbgdceah")
    args = parser.parse_args()

    operations = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(operations, starting=args.password)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(operations, scrambled=args.scrambled)}")


if __name__ == "__main__":
    main()
