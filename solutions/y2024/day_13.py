from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, NamedTuple


class Machine(NamedTuple):
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int


MACHINE_PATTERN = re.compile(
    r"Button A: X\+(?P<ax>\d+), Y\+(?P<ay>\d+)\n"
    r"Button B: X\+(?P<bx>\d+), Y\+(?P<by>\d+)\n"
    r"Prize: X=(?P<px>\d+), Y=(?P<py>\d+)"
)


def parse(raw: str) -> list[Machine]:
    machines: list[Machine] = []
    for block in raw.strip().split("\n\n"):
        match = MACHINE_PATTERN.match(block.strip())
        if not match:
            continue
        machines.append(
            Machine(
                ax=int(match.group("ax")),
                ay=int(match.group("ay")),
                bx=int(match.group("bx")),
                by=int(match.group("by")),
                px=int(match.group("px")),
                py=int(match.group("py")),
            )
        )
    return machines


def cheapest_tokens_with_limits(machine: Machine, limit: int = 100) -> int | None:
    best_cost: int | None = None
    ax, ay, bx, by, px, py = machine

    for a_presses in range(limit + 1):
        remaining_x = px - ax * a_presses
        remaining_y = py - ay * a_presses
        if remaining_x < 0 or remaining_y < 0:
            continue
        if bx == 0 or by == 0:
            if remaining_x == 0 and remaining_y == 0:
                cost = 3 * a_presses
                best_cost = cost if best_cost is None or cost < best_cost else best_cost
            continue
        if remaining_x % bx != 0 or remaining_y % by != 0:
            continue
        b_presses = remaining_x // bx
        if b_presses != remaining_y // by or b_presses > limit:
            continue
        cost = 3 * a_presses + b_presses
        if best_cost is None or cost < best_cost:
            best_cost = cost
    return best_cost


def solve_part1(machines: Iterable[Machine]) -> int:
    total = 0
    for machine in machines:
        cost = cheapest_tokens_with_limits(machine)
        if cost is not None:
            total += cost
    return total


def solve_machine_with_offset(machine: Machine, offset: int) -> int | None:
    ax, ay, bx, by, px, py = machine
    prize_x = px + offset
    prize_y = py + offset

    determinant = ax * by - ay * bx
    if determinant == 0:
        return None

    numerator_a = prize_x * by - prize_y * bx
    numerator_b = ax * prize_y - ay * prize_x

    if numerator_a % determinant != 0 or numerator_b % determinant != 0:
        return None

    a_presses = numerator_a // determinant
    b_presses = numerator_b // determinant

    if a_presses < 0 or b_presses < 0:
        return None

    return 3 * a_presses + b_presses


def solve_part2(machines: Iterable[Machine]) -> int:
    total = 0
    offset = 10_000_000_000_000
    for machine in machines:
        cost = solve_machine_with_offset(machine, offset)
        if cost is not None:
            total += cost
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 13.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    machines = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(machines)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(machines)}")


if __name__ == "__main__":
    main()
