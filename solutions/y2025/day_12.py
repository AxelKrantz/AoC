from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Shape:
    cells: tuple[tuple[int, int], ...]
    width: int
    height: int


@dataclass(frozen=True)
class Region:
    width: int
    height: int
    counts: tuple[int, ...]


ParsedInput = tuple[list[Shape], list[Region]]


def parse(raw: str) -> ParsedInput:
    lines = raw.strip().splitlines()
    shapes_by_index: dict[int, Shape] = {}
    regions: list[Region] = []

    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue
        if "x" in line:
            break
        shape_idx = int(line.rstrip(":"))
        idx += 1
        shape_rows: list[str] = []
        while idx < len(lines) and lines[idx].strip():
            shape_rows.append(lines[idx])
            idx += 1
        cells: list[tuple[int, int]] = []
        for y, row in enumerate(shape_rows):
            for x, ch in enumerate(row):
                if ch == "#":
                    cells.append((x, y))
        width = max(x for x, _ in cells) + 1
        height = max(y for _, y in cells) + 1
        shapes_by_index[shape_idx] = Shape(tuple(cells), width, height)
        idx += 1  # consume trailing blank line if present

    shapes = [shape for _, shape in sorted(shapes_by_index.items())]

    for line in lines[idx:]:
        if not line.strip():
            continue
        dims, counts_str = line.split(":")
        width_str, height_str = dims.split("x")
        counts = tuple(int(value) for value in counts_str.strip().split())
        regions.append(Region(int(width_str), int(height_str), counts))

    return shapes, regions


def _normalize(cells: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    coords = list(cells)
    min_x = min(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    return tuple(sorted((x - min_x, y - min_y) for x, y in coords))


def orientations(shape: Shape) -> tuple[Shape, ...]:
    seen: set[tuple[tuple[int, int], ...]] = set()
    for flip in (1, -1):
        for rotation in range(4):
            coords: list[tuple[int, int]] = []
            for x, y in shape.cells:
                x, y = x, y * flip
                for _ in range(rotation):
                    x, y = -y, x
                coords.append((x, y))
            seen.add(_normalize(coords))

    # Mirror across the x-axis and rotate again to capture reflections.
    mirrored = [(-x, y) for x, y in shape.cells]
    for rotation in range(4):
        coords: list[tuple[int, int]] = []
        for x, y in mirrored:
            for _ in range(rotation):
                x, y = -y, x
            coords.append((x, y))
        seen.add(_normalize(coords))

    result = []
    for coords in seen:
        width = max(x for x, _ in coords) + 1
        height = max(y for _, y in coords) + 1
        result.append(Shape(coords, width, height))
    return tuple(result)


def _generate_placements(shape: Shape, width: int, height: int) -> list[int]:
    placements: list[int] = []
    for oriented in orientations(shape):
        max_x = width - oriented.width
        max_y = height - oriented.height
        if max_x < 0 or max_y < 0:
            continue
        for dy in range(max_y + 1):
            for dx in range(max_x + 1):
                mask = 0
                for x, y in oriented.cells:
                    idx = (y + dy) * width + (x + dx)
                    mask |= 1 << idx
                placements.append(mask)
    return list(set(placements))


def _can_place_exact(shapes: Sequence[Shape], region: Region) -> bool:
    width, height = region.width, region.height
    total_cells = sum(len(shapes[i].cells) * count for i, count in enumerate(region.counts))
    if total_cells > width * height:
        return False

    pieces: list[int] = []
    for idx, count in enumerate(region.counts):
        pieces.extend([idx] * count)
    if not pieces:
        return True

    placements_by_shape = [_generate_placements(shape, width, height) for shape in shapes]
    pieces.sort(key=lambda idx: len(placements_by_shape[idx]))
    memo: dict[tuple[int, int], bool] = {}

    def dfs(piece_idx: int, occupied: int) -> bool:
        state = (piece_idx, occupied)
        if state in memo:
            return memo[state]
        if piece_idx == len(pieces):
            return True
        shape_idx = pieces[piece_idx]
        for placement in placements_by_shape[shape_idx]:
            if placement & occupied:
                continue
            if dfs(piece_idx + 1, occupied | placement):
                memo[state] = True
                return True
        memo[state] = False
        return False

    return dfs(0, 0)


def can_fit_region(shapes: Sequence[Shape], region: Region) -> bool:
    width, height = region.width, region.height
    total_cells = sum(
        len(shapes[i].cells) * count for i, count in enumerate(region.counts)
    )
    if total_cells > width * height:
        return False

    max_w = max(shape.width for shape in shapes)
    max_h = max(shape.height for shape in shapes)
    for shape, count in zip(shapes, region.counts):
        if count and (shape.width > width or shape.height > height):
            return False

    block_capacity = (width // max_w) * (height // max_h)
    total_shapes = sum(region.counts)
    if total_shapes <= block_capacity:
        return True

    if width * height <= 80 and total_shapes <= 12:
        return _can_place_exact(shapes, region)
    return False


def solve_part1(parsed: ParsedInput) -> int:
    shapes, regions = parsed
    return sum(1 for region in regions if can_fit_region(shapes, region))


def solve_part2(_: ParsedInput) -> int:
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2025 Day 12.")
    parser.add_argument("input_path", type=Path, help="Path to puzzle input.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args(list(argv) if argv is not None else None)

    parsed = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(parsed)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(parsed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
