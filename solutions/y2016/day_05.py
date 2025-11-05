from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def parse(raw: str) -> str:
    return raw.strip()


def find_hashes(door_id: str) -> tuple[str, str]:
    password1: list[str] = []
    password2 = ["_"] * 8
    filled = 0
    index = 0
    while len(password1) < 8 or filled < 8:
        digest = hashlib.md5(f"{door_id}{index}".encode("utf-8")).hexdigest()
        if digest.startswith("00000"):
            if len(password1) < 8:
                password1.append(digest[5])
            pos_char = digest[5]
            if pos_char.isdigit():
                position = int(pos_char)
                if 0 <= position < 8 and password2[position] == "_":
                    password2[position] = digest[6]
                    filled += 1
        index += 1
    return "".join(password1), "".join(password2)


def solve_part1(door_id: str) -> str:
    return find_hashes(door_id)[0]


def solve_part2(door_id: str) -> str:
    return find_hashes(door_id)[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 5.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    door_id = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(door_id)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(door_id)}")


if __name__ == "__main__":
    main()
