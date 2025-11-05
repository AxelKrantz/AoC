from __future__ import annotations

import argparse
import functools
import hashlib
import re
from pathlib import Path

TRIPLE_RE = re.compile(r"(.)\1\1")


def parse(raw: str) -> str:
    return raw.strip()


@functools.lru_cache(maxsize=None)
def compute_hash(salt: str, index: int, stretch: int) -> str:
    digest = hashlib.md5(f"{salt}{index}".encode("utf-8")).hexdigest()
    for _ in range(stretch):
        digest = hashlib.md5(digest.encode("utf-8")).hexdigest()
    return digest


def nth_key_index(salt: str, count: int = 64, stretch: int = 0) -> int:
    found = 0
    index = 0
    while True:
        digest = compute_hash(salt, index, stretch)
        match = TRIPLE_RE.search(digest)
        if match:
            target = match.group(1) * 5
            for future in range(index + 1, index + 1001):
                future_digest = compute_hash(salt, future, stretch)
                if target in future_digest:
                    found += 1
                    if found == count:
                        return index
                    break
        index += 1


def solve_part1(salt: str) -> int:
    compute_hash.cache_clear()
    return nth_key_index(salt, count=64, stretch=0)


def solve_part2(salt: str) -> int:
    compute_hash.cache_clear()
    return nth_key_index(salt, count=64, stretch=2016)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 14.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    salt = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(salt)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(salt)}")


if __name__ == "__main__":
    main()
