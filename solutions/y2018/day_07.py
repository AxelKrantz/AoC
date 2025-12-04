from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

import re

DEPENDENCY_PATTERN = re.compile(
    r"Step (?P<before>[A-Z]) must be finished before step (?P<after>[A-Z]) can begin\."
)

Edge = tuple[str, str]


def parse(raw: str) -> list[Edge]:
    edges: list[Edge] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = DEPENDENCY_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"Unable to parse instruction: {line!r}")
        edges.append((match.group("before"), match.group("after")))
    return edges


def build_prerequisites(edges: Iterable[Edge]) -> dict[str, set[str]]:
    prerequisites: dict[str, set[str]] = {}
    for before, after in edges:
        prerequisites.setdefault(before, set())
        prerequisites.setdefault(after, set()).add(before)
    return prerequisites


def solve_part1(edges: Sequence[Edge]) -> str:
    prerequisites = build_prerequisites(edges)
    completed: list[str] = []

    while prerequisites:
        available = sorted(
            step for step, deps in prerequisites.items() if deps.issubset(completed)
        )
        if not available:
            raise RuntimeError("Cyclic dependency detected.")
        current = available[0]
        completed.append(current)
        prerequisites.pop(current)
    return "".join(completed)


def task_duration(step: str, base_duration: int) -> int:
    return base_duration + (ord(step) - ord("A") + 1)


def solve_part2(
    edges: Sequence[Edge], worker_count: int = 5, base_duration: int = 60
) -> int:
    prerequisites = build_prerequisites(edges)
    in_progress: dict[str, int] = {}
    completed: list[str] = []
    time = 0

    while len(completed) < len(prerequisites):
        available_steps = sorted(
            step
            for step, deps in prerequisites.items()
            if step not in in_progress
            and step not in completed
            and deps.issubset(completed)
        )
        while available_steps and len(in_progress) < worker_count:
            step = available_steps.pop(0)
            in_progress[step] = task_duration(step, base_duration)

        if not in_progress:
            raise RuntimeError("No tasks in progress despite remaining work.")

        advance = min(in_progress.values())
        time += advance
        finished = []
        for step in list(in_progress):
            remaining = in_progress[step] - advance
            if remaining == 0:
                finished.append(step)
                in_progress.pop(step)
            else:
                in_progress[step] = remaining

        completed.extend(sorted(finished))

    return time


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 7.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    edges = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(edges)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(edges)}")


if __name__ == "__main__":
    main()
