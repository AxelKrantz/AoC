from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence


def parse(raw: str) -> list[str]:
    return [line.strip() for line in raw.strip().splitlines() if line.strip()]


def solve_part1(box_ids: Iterable[str]) -> int:
    twos = 0
    threes = 0
    for box_id in box_ids:
        counts = Counter(box_id)
        if any(count == 2 for count in counts.values()):
            twos += 1
        if any(count == 3 for count in counts.values()):
            threes += 1
    return twos * threes


def common_letters(id1: str, id2: str) -> str | None:
    mismatch = 0
    common_chars: list[str] = []
    for ch1, ch2 in zip(id1, id2):
        if ch1 == ch2:
            common_chars.append(ch1)
        else:
            mismatch += 1
            if mismatch > 1:
                return None
    if mismatch == 1 and len(id1) == len(id2):
        return "".join(common_chars)
    return None


def solve_part2(box_ids: Sequence[str]) -> str:
    length = len(box_ids)
    for i in range(length):
        for j in range(i + 1, length):
            common = common_letters(box_ids[i], box_ids[j])
            if common:
                return common
    raise RuntimeError("No box IDs found that differ by exactly one character.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 2.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    box_ids = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(box_ids)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(box_ids)}")


if __name__ == "__main__":
    main()
