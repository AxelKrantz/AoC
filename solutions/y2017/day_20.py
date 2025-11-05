from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


PARTICLE_RE = re.compile(r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>")


@dataclass
class Particle:
    position: List[int]
    velocity: List[int]
    acceleration: List[int]


def parse(raw: str) -> Dict[int, Particle]:
    particles: dict[int, Particle] = {}
    for index, line in enumerate(raw.strip().splitlines()):
        match = PARTICLE_RE.fullmatch(line.strip())
        if not match:
            continue
        values = list(map(int, match.groups()))
        particles[index] = Particle(
            position=values[0:3],
            velocity=values[3:6],
            acceleration=values[6:9],
        )
    return particles


def manhattan(vector: List[int]) -> int:
    return sum(abs(component) for component in vector)


def solve_part1(particles: Dict[int, Particle]) -> int:
    return min(
        particles.items(),
        key=lambda item: (
            manhattan(item[1].acceleration),
            manhattan(item[1].velocity),
            manhattan(item[1].position),
        ),
    )[0]


def simulate_collisions(particles: Dict[int, Particle], steps: int = 1000) -> int:
    active = {index: Particle(p.position[:], p.velocity[:], p.acceleration[:]) for index, p in particles.items()}
    for _ in range(steps):
        positions: dict[int, Tuple[int, int, int]] = {}
        for index, particle in active.items():
            for i in range(3):
                particle.velocity[i] += particle.acceleration[i]
                particle.position[i] += particle.velocity[i]
            positions[index] = tuple(particle.position)
        counts = Counter(positions.values())
        active = {index: particle for index, particle in active.items() if counts[positions[index]] == 1}
    return len(active)


def solve_part2(particles: Dict[int, Particle]) -> int:
    return simulate_collisions(particles)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 20.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--steps", type=int, default=1000)
    args = parser.parse_args()

    particles = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(particles)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {simulate_collisions(particles, steps=args.steps)}")


if __name__ == "__main__":
    main()
