from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, Tuple


def parse(raw: str) -> list[tuple[list[str], list[str]]]:
    addresses: list[tuple[list[str], list[str]]] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        supernets: list[str] = []
        hypernets: list[str] = []
        parts = re.split(r"(\[|\])", line)
        in_brackets = False
        buffer = ""
        for part in parts:
            if part == "[":
                if buffer:
                    supernets.append(buffer)
                    buffer = ""
                in_brackets = True
            elif part == "]":
                if buffer:
                    hypernets.append(buffer)
                    buffer = ""
                in_brackets = False
            else:
                buffer += part
        if buffer:
            (hypernets if in_brackets else supernets).append(buffer)
        addresses.append((supernets, hypernets))
    return addresses


def has_abba(sequence: str) -> bool:
    return any(
        a != b and sequence[i : i + 4] == a + b + b + a
        for i in range(len(sequence) - 3)
        for a, b in [(sequence[i], sequence[i + 1])]
    )


def supports_tls(supernets: Iterable[str], hypernets: Iterable[str]) -> bool:
    return any(has_abba(sn) for sn in supernets) and not any(has_abba(hn) for hn in hypernets)


def find_aba(sequence: str) -> List[str]:
    abas: list[str] = []
    for i in range(len(sequence) - 2):
        a, b, c = sequence[i : i + 3]
        if a == c and a != b:
            abas.append(sequence[i : i + 3])
    return abas


def supports_ssl(supernets: Iterable[str], hypernets: Iterable[str]) -> bool:
    abas = []
    for sn in supernets:
        abas.extend(find_aba(sn))
    desired = {aba[1] + aba[0] + aba[1] for aba in abas}
    for hn in hypernets:
        for bab in desired:
            if bab in hn:
                return True
    return False


def solve_part1(addresses: Iterable[tuple[list[str], list[str]]]) -> int:
    return sum(1 for supernets, hypernets in addresses if supports_tls(supernets, hypernets))


def solve_part2(addresses: Iterable[tuple[list[str], list[str]]]) -> int:
    return sum(1 for supernets, hypernets in addresses if supports_ssl(supernets, hypernets))


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 7.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    addresses = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(addresses)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(addresses)}")


if __name__ == "__main__":
    main()
