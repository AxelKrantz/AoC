from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Reindeer:
    name: str
    speed: int
    fly_time: int
    rest_time: int


def parse(raw: str) -> list[Reindeer]:
    reindeer: list[Reindeer] = []
    for line in raw.strip().splitlines():
        parts = line.split()
        name = parts[0]
        speed = int(parts[3])
        fly_time = int(parts[6])
        rest_time = int(parts[-2])
        reindeer.append(Reindeer(name, speed, fly_time, rest_time))
    return reindeer


def distance_after(reindeer: Reindeer, duration: int) -> int:
    cycle = reindeer.fly_time + reindeer.rest_time
    full_cycles, remainder = divmod(duration, cycle)
    distance = full_cycles * reindeer.speed * reindeer.fly_time
    distance += reindeer.speed * min(remainder, reindeer.fly_time)
    return distance


def solve_part1(reindeer: Iterable[Reindeer], duration: int = 2503) -> int:
    return max(distance_after(r, duration) for r in reindeer)


def solve_part2(reindeer: list[Reindeer], duration: int = 2503) -> int:
    scores = {r.name: 0 for r in reindeer}
    distances = {r.name: 0 for r in reindeer}

    for second in range(1, duration + 1):
        for r in reindeer:
            distances[r.name] = distance_after(r, second)
        lead = max(distances.values())
        for name, distance in distances.items():
            if distance == lead:
                scores[name] += 1

    return max(scores.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 14.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--duration", type=int, default=2503)
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    herd = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(herd, args.duration)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(herd, args.duration)}")


if __name__ == "__main__":
    main()
