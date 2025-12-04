from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


CLAIM_PATTERN = re.compile(
    r"#(?P<claim_id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)"
)


@dataclass(frozen=True)
class Claim:
    claim_id: int
    left: int
    top: int
    width: int
    height: int

    def coordinates(self) -> Iterable[tuple[int, int]]:
        for x in range(self.left, self.left + self.width):
            for y in range(self.top, self.top + self.height):
                yield (x, y)


def parse(raw: str) -> list[Claim]:
    claims: list[Claim] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = CLAIM_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"Unable to parse claim line: {line!r}")
        claims.append(
            Claim(
                claim_id=int(match.group("claim_id")),
                left=int(match.group("left")),
                top=int(match.group("top")),
                width=int(match.group("width")),
                height=int(match.group("height")),
            )
        )
    return claims


def compute_fabric_counts(claims: Iterable[Claim]) -> dict[tuple[int, int], int]:
    fabric: dict[tuple[int, int], int] = {}
    for claim in claims:
        for coord in claim.coordinates():
            fabric[coord] = fabric.get(coord, 0) + 1
    return fabric


def solve_part1(claims: Sequence[Claim]) -> int:
    fabric = compute_fabric_counts(claims)
    return sum(1 for count in fabric.values() if count > 1)


def solve_part2(claims: Sequence[Claim]) -> int:
    fabric = compute_fabric_counts(claims)
    for claim in claims:
        if all(fabric[coord] == 1 for coord in claim.coordinates()):
            return claim.claim_id
    raise RuntimeError("No non-overlapping claim found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 3.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    claims = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(claims)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(claims)}")


if __name__ == "__main__":
    main()

