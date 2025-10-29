from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple

Box = Tuple[int, int, int]


def parse(raw: str) -> list[Box]:
    boxes: list[Box] = []
    for line in raw.splitlines():
        if not line:
            continue
        parts = line.split("x")
        if len(parts) != 3:
            raise ValueError(f"Invalid dimensions: {line}")
        l, w, h = map(int, parts)
        boxes.append((l, w, h))
    return boxes


def surface_area_with_slack(box: Box) -> int:
    l, w, h = box
    sides = (l * w, w * h, h * l)
    return 2 * sum(sides) + min(sides)


def ribbon_length(box: Box) -> int:
    l, w, h = sorted(box)
    perimeter = 2 * (l + w)
    volume = l * w * h
    return perimeter + volume


def solve_part1(boxes: Iterable[Box]) -> int:
    return sum(surface_area_with_slack(box) for box in boxes)


def solve_part2(boxes: Iterable[Box]) -> int:
    return sum(ribbon_length(box) for box in boxes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 2.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    boxes = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(boxes)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(boxes)}")


if __name__ == "__main__":
    main()
