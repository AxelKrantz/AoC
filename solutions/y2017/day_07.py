from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


LINE_RE = re.compile(r"(?P<name>\w+) \((?P<weight>\d+)\)(?: -> (?P<children>.*))?")


@dataclass(frozen=True)
class Program:
    weight: int
    children: list[str]


def parse(raw: str) -> dict[str, Program]:
    programs: dict[str, Program] = {}
    for line in raw.strip().splitlines():
        match = LINE_RE.fullmatch(line.strip())
        if not match:
            continue
        name = match.group("name")
        weight = int(match.group("weight"))
        children = match.group("children")
        programs[name] = Program(weight=weight, children=children.split(", ") if children else [])
    return programs


def find_root(programs: Dict[str, Program]) -> str:
    all_children = {child for program in programs.values() for child in program.children}
    for name in programs:
        if name not in all_children:
            return name
    raise ValueError("Root not found.")


class ImbalanceFound(Exception):
    def __init__(self, corrected_weight: int) -> None:
        self.corrected_weight = corrected_weight
        super().__init__(str(corrected_weight))


def total_weight(name: str, programs: Dict[str, Program]) -> int:
    program = programs[name]
    if not program.children:
        return program.weight
    weights: dict[int, list[str]] = {}
    child_totals: dict[str, int] = {}
    for child in program.children:
        child_total = total_weight(child, programs)
        child_totals[child] = child_total
        weights.setdefault(child_total, []).append(child)

    if len(weights) > 1:
        correct_total = max(weights.items(), key=lambda item: len(item[1]))[0]
        wrong_total, wrong_children = min(weights.items(), key=lambda item: len(item[1]))
        wrong_child = wrong_children[0]
        difference = correct_total - wrong_total
        corrected_weight = programs[wrong_child].weight + difference
        raise ImbalanceFound(corrected_weight)

    return program.weight + sum(child_totals.values())


def solve_part1(programs: Dict[str, Program]) -> str:
    return find_root(programs)


def solve_part2(programs: Dict[str, Program]) -> int:
    root = find_root(programs)
    try:
        total_weight(root, programs)
    except ImbalanceFound as exc:
        return exc.corrected_weight
    raise ValueError("No imbalance detected.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 7.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    programs = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(programs)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(programs)}")


if __name__ == "__main__":
    main()
