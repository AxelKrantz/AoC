from __future__ import annotations

import argparse
import re
from collections import deque
from pathlib import Path
from typing import Iterable

Replacement = tuple[str, str]


TOKEN_REGEX = re.compile(r"[A-Z][a-z]*")


def parse(raw: str) -> tuple[list[Replacement], str]:
    lines = [line for line in raw.strip().splitlines() if line]
    molecule = lines[-1]
    replacements: list[Replacement] = []
    for line in lines[:-1]:
        source, target = line.split(" => ")
        replacements.append((source, target))
    return replacements, molecule


def distinct_molecules(replacements: Iterable[Replacement], molecule: str) -> int:
    results: set[str] = set()
    for source, target in replacements:
        start = 0
        while True:
            index = molecule.find(source, start)
            if index == -1:
                break
            new_molecule = (
                molecule[:index] + target + molecule[index + len(source) :]
            )
            results.add(new_molecule)
            start = index + 1
    return len(results)


def tokenize(molecule: str) -> list[str]:
    return TOKEN_REGEX.findall(molecule)


def minimal_steps_formula(molecule: str) -> int:
    tokens = tokenize(molecule)
    rn = tokens.count("Rn")
    ar = tokens.count("Ar")
    y = tokens.count("Y")
    return len(tokens) - rn - ar - 2 * y - 1


def minimal_steps_bfs(replacements: list[Replacement], molecule: str) -> int:
    reverse = [(target, source) for source, target in replacements]
    queue = deque([(molecule, 0)])
    visited = {molecule}
    while queue:
        current, steps = queue.popleft()
        if current == "e":
            return steps
        for target, source in reverse:
            start = 0
            while True:
                index = current.find(target, start)
                if index == -1:
                    break
                candidate = current[:index] + source + current[index + len(target) :]
                if candidate not in visited:
                    visited.add(candidate)
                    queue.append((candidate, steps + 1))
                start = index + 1
    raise ValueError("Unable to reduce molecule to 'e'.")


def solve_part1(data: tuple[list[Replacement], str]) -> int:
    replacements, molecule = data
    return distinct_molecules(replacements, molecule)


def solve_part2(data: tuple[list[Replacement], str]) -> int:
    replacements, molecule = data
    tokens = tokenize(molecule)
    if len(tokens) <= 16:
        return minimal_steps_bfs(replacements, molecule)
    return minimal_steps_formula(molecule)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 19.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    data = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
