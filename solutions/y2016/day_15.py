from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Disc:
    positions: int
    start: int


DISC_RE = re.compile(
    r"Disc #(?P<index>\d+) has (?P<positions>\d+) positions; at time=0, it is at position (?P<start>\d+)."
)


def parse(raw: str) -> List[Disc]:
    discs: list[Disc] = []
    for line in raw.strip().splitlines():
        match = DISC_RE.match(line.strip())
        if not match:
            continue
        discs.append(
            Disc(
                positions=int(match.group("positions")),
                start=int(match.group("start")),
            )
        )
    return discs


def find_time(discs: Iterable[Disc]) -> int:
    time = 0
    step = 1
    for index, disc in enumerate(discs, start=1):
        while (disc.start + index + time) % disc.positions != 0:
            time += step
        step = math.lcm(step, disc.positions)
    return time


def solve_part1(discs: Iterable[Disc]) -> int:
    return find_time(list(discs))


def solve_part2(discs: List[Disc]) -> int:
    extended = discs + [Disc(positions=11, start=0)]
    return find_time(extended)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 15.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    discs = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(discs)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(discs)}")


if __name__ == "__main__":
    main()
