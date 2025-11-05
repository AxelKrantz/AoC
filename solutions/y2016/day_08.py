from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set, Tuple


@dataclass(frozen=True)
class Instruction:
    type: str
    a: int
    b: int | None = None


def parse(raw: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("rect"):
            _, size = line.split()
            width, height = map(int, size.split("x"))
            instructions.append(Instruction("rect", width, height))
        elif line.startswith("rotate row"):
            parts = line.split()
            y = int(parts[2].split("=")[1])
            shift = int(parts[-1])
            instructions.append(Instruction("rotate_row", y, shift))
        elif line.startswith("rotate column"):
            parts = line.split()
            x = int(parts[2].split("=")[1])
            shift = int(parts[-1])
            instructions.append(Instruction("rotate_column", x, shift))
        else:
            raise ValueError(f"Unknown instruction: {line}")
    return instructions


def apply(instructions: Iterable[Instruction], width: int = 50, height: int = 6) -> Set[Tuple[int, int]]:
    pixels: set[tuple[int, int]] = set()
    for instruction in instructions:
        if instruction.type == "rect":
            assert instruction.b is not None
            for x in range(instruction.a):
                for y in range(instruction.b):
                    pixels.add((x, y))
        elif instruction.type == "rotate_row":
            y = instruction.a
            shift = instruction.b or 0
            row_pixels = {(x, yy) for x, yy in pixels if yy == y}
            pixels.difference_update(row_pixels)
            for x, _ in row_pixels:
                pixels.add(((x + shift) % width, y))
        elif instruction.type == "rotate_column":
            x = instruction.a
            shift = instruction.b or 0
            column_pixels = {(xx, y) for xx, y in pixels if xx == x}
            pixels.difference_update(column_pixels)
            for _, y in column_pixels:
                pixels.add((x, (y + shift) % height))
        else:
            raise ValueError(f"Unsupported instruction type: {instruction.type}")
    return pixels


def render(pixels: Set[Tuple[int, int]], width: int = 50, height: int = 6) -> str:
    rows: List[str] = []
    for y in range(height):
        row = "".join("#" if (x, y) in pixels else "." for x in range(width))
        rows.append(row)
    return "\n".join(rows)


LETTER_SHAPES = {
    "A": (".##.", "#..#", "#..#", "####", "#..#", "#..#"),
    "B": ("###.", "#..#", "###.", "#..#", "#..#", "###."),
    "C": (".##.", "#..#", "#...", "#...", "#..#", ".##."),
    "E": ("####", "#...", "###.", "#...", "#...", "####"),
    "F": ("####", "#...", "###.", "#...", "#...", "#..."),
    "G": (".##.", "#..#", "#...", "#.##", "#..#", ".###"),
    "H": ("#..#", "#..#", "####", "#..#", "#..#", "#..#"),
    "I": ("###", ".#.", ".#.", ".#.", ".#.", "###"),
    "J": ("..##", "...#", "...#", "...#", "#..#", ".##."),
    "K": ("#..#", "#.#.", "##..", "#.#.", "#.#.", "#..#"),
    "L": ("#...", "#...", "#...", "#...", "#...", "####"),
    "O": (".##.", "#..#", "#..#", "#..#", "#..#", ".##."),
    "P": ("###.", "#..#", "#..#", "###.", "#...", "#..."),
    "R": ("###.", "#..#", "#..#", "###.", "#.#.", "#..#"),
    "U": ("#..#", "#..#", "#..#", "#..#", "#..#", ".##."),
    "Y": ("#...#", "#...#", ".###.", "..#..", "..#..", "..#.."),
    "Z": ("####", "...#", "..#.", ".#..", "#...", "####"),
}


def _build_letter_patterns() -> dict[str, str]:
    patterns: dict[str, str] = {}
    for letter, rows in LETTER_SHAPES.items():
        width = max(len(row) for row in rows)
        normalized = "".join(row.ljust(width, ".") for row in rows)
        patterns[normalized] = letter
    return patterns


LETTER_PATTERNS = _build_letter_patterns()


def decode_message(pixels: Set[Tuple[int, int]], width: int, height: int) -> str:
    rows = ["".join("#" if (x, y) in pixels else "." for x in range(width)) for y in range(height)]
    letters: List[str] = []
    x = 0
    while x < width:
        if all(row[x] == "." for row in rows):
            x += 1
            continue
        start = x
        while x < width and any(row[x] == "#" for row in rows):
            x += 1
        block_rows = [row[start:x] for row in rows]
        max_len = max(len(line) for line in block_rows)
        normalized = "".join(line.ljust(max_len, ".") for line in block_rows)
        letter = LETTER_PATTERNS.get(normalized)
        if letter is None:
            raise ValueError(f"Unrecognized letter pattern: {normalized}")
        letters.append(letter)
    return "".join(letters)


def solve_part1(instructions: Iterable[Instruction], width: int = 50, height: int = 6) -> int:
    pixels = apply(instructions, width=width, height=height)
    return len(pixels)


def solve_part2(instructions: Iterable[Instruction], width: int = 50, height: int = 6) -> str:
    pixels = apply(instructions, width=width, height=height)
    return decode_message(pixels, width=width, height=height)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 8.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--width", type=int, default=50)
    parser.add_argument("--height", type=int, default=6)
    args = parser.parse_args()

    instructions = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(instructions, width=args.width, height=args.height)}")
    if args.part in {"2", "both"}:
        pixels = apply(instructions, width=args.width, height=args.height)
        message = decode_message(pixels, width=args.width, height=args.height)
        print(f"Part 2: {message}")
        print(render(pixels, width=args.width, height=args.height))


if __name__ == "__main__":
    main()
