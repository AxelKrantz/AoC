from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Sequence, Tuple


Point = tuple[int, int, int, int]


def parse(raw: str) -> List[Point]:
    points: list[Point] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        points.append(tuple(int(value) for value in line.split(",")))
    return points


def manhattan_distance(a: Point, b: Point) -> int:
    return sum(abs(ai - bi) for ai, bi in zip(a, b))


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, a: int, b: int) -> None:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def solve_part1(points: Sequence[Point]) -> int:
    dsu = DisjointSet(len(points))
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            if manhattan_distance(point, points[j]) <= 3:
                dsu.union(i, j)
    roots = {dsu.find(index) for index in range(len(points))}
    return len(roots)


def solve_part2(_points: Sequence[Point]) -> int:
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 25.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    data = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(data)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(data)}")


if __name__ == "__main__":
    main()
