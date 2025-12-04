from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Set, Tuple


SPREAD_RANGE = 2


@dataclass(frozen=True)
class Notes:
    initial: Set[int]
    rules: Dict[str, str]


def parse(raw: str) -> Notes:
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    initial_line = lines[0]
    state = initial_line.split(": ")[1]
    initial = {idx for idx, pot in enumerate(state) if pot == "#"}
    rules: Dict[str, str] = {}
    for line in lines[1:]:
        pattern, result = line.split(" => ")
        rules[pattern] = result
    return Notes(initial=initial, rules=rules)


def evolve(state: Set[int], rules: Dict[str, str]) -> Set[int]:
    if not state:
        return set()
    new_state: Set[int] = set()
    min_idx = min(state)
    max_idx = max(state)
    for idx in range(min_idx - SPREAD_RANGE, max_idx + SPREAD_RANGE + 1):
        pattern = "".join("#" if (idx + offset) in state else "." for offset in range(-2, 3))
        if rules.get(pattern, ".") == "#":
            new_state.add(idx)
    return new_state


def simulate(notes: Notes, generations: int) -> int:
    state = set(notes.initial)
    for _ in range(generations):
        state = evolve(state, notes.rules)
    return sum(state)


def solve_part1(notes: Notes) -> int:
    return simulate(notes, 20)


def solve_part2(notes: Notes, generations: int = 50_000_000_000) -> int:
    state = set(notes.initial)
    last_sum = sum(state)
    last_delta = None
    stable_steps = 0
    for generation in range(1, generations + 1):
        state = evolve(state, notes.rules)
        current_sum = sum(state)
        delta = current_sum - last_sum
        if delta == last_delta:
            stable_steps += 1
            if stable_steps >= 5:
                remaining = generations - generation
                return current_sum + remaining * delta
        else:
            stable_steps = 0
            last_delta = delta
        last_sum = current_sum
    return last_sum


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 12.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--generations", type=int, default=50_000_000_000)
    args = parser.parse_args()

    notes = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(notes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(notes, args.generations)}")


if __name__ == "__main__":
    main()

