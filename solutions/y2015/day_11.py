from __future__ import annotations

import argparse
from pathlib import Path


FORBIDDEN = {"i", "o", "l"}


def parse(raw: str) -> str:
    return raw.strip()


def increment(password: str) -> str:
    chars = list(password)
    index = len(chars) - 1
    while index >= 0:
        if chars[index] == "z":
            chars[index] = "a"
            index -= 1
        else:
            chars[index] = chr(ord(chars[index]) + 1)
            break
    return "".join(chars)


def has_straight(password: str) -> bool:
    for a, b, c in zip(password, password[1:], password[2:]):
        if ord(a) + 1 == ord(b) and ord(b) + 1 == ord(c):
            return True
    return False


def has_no_forbidden(password: str) -> bool:
    return all(char not in FORBIDDEN for char in password)


def has_two_pairs(password: str) -> bool:
    pairs = set()
    index = 0
    while index < len(password) - 1:
        if password[index] == password[index + 1]:
            pairs.add(password[index])
            index += 2
        else:
            index += 1
    return len(pairs) >= 2


def is_valid(password: str) -> bool:
    return has_straight(password) and has_no_forbidden(password) and has_two_pairs(password)


def next_password(password: str) -> str:
    candidate = increment(password)
    while not is_valid(candidate):
        candidate = increment(candidate)
    return candidate


def solve_part1(password: str) -> str:
    return next_password(password)


def solve_part2(password: str) -> str:
    first = next_password(password)
    return next_password(first)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 11.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    password = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(password)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(password)}")


if __name__ == "__main__":
    main()
