from __future__ import annotations

import argparse
import collections
import string
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Room:
    name: str
    sector_id: int
    checksum: str


def parse(raw: str) -> list[Room]:
    rooms: list[Room] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        name_part, rest = line.rsplit("-", 1)
        sector_str, checksum_part = rest.split("[")
        checksum = checksum_part.rstrip("]")
        rooms.append(Room(name=name_part, sector_id=int(sector_str), checksum=checksum))
    return rooms


def compute_checksum(name: str) -> str:
    counter = collections.Counter(c for c in name if c != "-")
    items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return "".join(char for char, _ in items[:5])


def is_real(room: Room) -> bool:
    return compute_checksum(room.name) == room.checksum


def solve_part1(rooms: list[Room]) -> int:
    return sum(room.sector_id for room in rooms if is_real(room))


ALPHABET = string.ascii_lowercase


def decrypt(room: Room) -> str:
    shift = room.sector_id % 26
    translated: list[str] = []
    for char in room.name:
        if char == "-":
            translated.append(" ")
        else:
            index = (ALPHABET.index(char) + shift) % 26
            translated.append(ALPHABET[index])
    return "".join(translated)


def solve_part2(rooms: list[Room]) -> int:
    for room in rooms:
        if not is_real(room):
            continue
        if decrypt(room) == "northpole object storage":
            return room.sector_id
    raise ValueError("North Pole storage room not found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 4.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    rooms = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(rooms)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(rooms)}")


if __name__ == "__main__":
    main()
