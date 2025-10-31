from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

DiskMap = str
FileInfo = Dict[int, Tuple[int, int]]
Segment = List[int]


def parse(raw: str) -> DiskMap:
    return raw.strip()


def build_disk(disk_map: DiskMap) -> tuple[list[int | None], FileInfo, list[list[int]], int]:
    blocks: list[int | None] = []
    file_positions: FileInfo = {}
    free_segments: list[list[int]] = []

    position = 0
    file_id = 0
    is_file = True

    for ch in disk_map:
        length = int(ch)
        if is_file:
            current_id = file_id
            if length > 0:
                file_positions[current_id] = (position, length)
                blocks.extend([current_id] * length)
            file_id += 1
        else:
            if length > 0:
                free_segments.append([position, length])
                blocks.extend([None] * length)
        position += length
        is_file = not is_file

    total_length = position
    return blocks, file_positions, free_segments, total_length


def compact_blocks(blocks: list[int | None]) -> None:
    left = 0
    right = len(blocks) - 1
    while left < right:
        if blocks[left] is not None:
            left += 1
            continue
        if blocks[right] is None:
            right -= 1
            continue
        blocks[left] = blocks[right]
        blocks[right] = None
        left += 1
        right -= 1


def checksum_from_blocks(blocks: Iterable[int | None]) -> int:
    total = 0
    for index, value in enumerate(blocks):
        if value is not None:
            total += index * value
    return total


def merge_segments(segments: list[list[int]]) -> list[list[int]]:
    if not segments:
        return []
    segments.sort()
    merged: list[list[int]] = []
    for start, length in segments:
        if length <= 0:
            continue
        if not merged:
            merged.append([start, length])
            continue
        prev_start, prev_length = merged[-1]
        prev_end = prev_start + prev_length
        current_end = start + length
        if start <= prev_end:
            merged[-1][1] = max(prev_end, current_end) - prev_start
        else:
            merged.append([start, length])
    return merged


def solve_part1(disk_map: DiskMap) -> int:
    blocks, _, _, _ = build_disk(disk_map)
    compact_blocks(blocks)
    return checksum_from_blocks(blocks)


def solve_part2(disk_map: DiskMap) -> int:
    _, file_positions, free_segments, _ = build_disk(disk_map)
    free_segments = merge_segments(free_segments)

    for file_id in sorted(file_positions.keys(), reverse=True):
        start, length = file_positions[file_id]
        if length == 0:
            continue

        destination_index = None
        for index, (gap_start, gap_length) in enumerate(free_segments):
            if gap_start >= start:
                break
            if gap_length >= length:
                destination_index = index
                break

        if destination_index is None:
            continue

        gap_start, gap_length = free_segments.pop(destination_index)
        destination = gap_start
        gap_end = gap_start + gap_length

        fragments: list[list[int]] = []
        if destination > gap_start:
            fragments.append([gap_start, destination - gap_start])
        if destination + length < gap_end:
            fragments.append([destination + length, gap_end - (destination + length)])

        free_segments.extend(fragments)
        free_segments.append([start, length])
        free_segments = merge_segments(free_segments)

        file_positions[file_id] = (destination, length)

    total = 0
    for file_id, (start, length) in file_positions.items():
        for offset in range(length):
            total += (start + offset) * file_id
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 9.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    disk_map = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(disk_map)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(disk_map)}")


if __name__ == "__main__":
    main()
