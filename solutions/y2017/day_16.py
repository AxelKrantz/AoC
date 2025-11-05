from __future__ import annotations

import argparse
from pathlib import Path
from typing import List


def parse(raw: str) -> list[str]:
    return [move for move in raw.strip().split(",") if move]


def dance(programs: str, moves: List[str]) -> str:
    lineup = list(programs)
    for move in moves:
        if move[0] == "s":
            size = int(move[1:])
            lineup = lineup[-size:] + lineup[:-size]
        elif move[0] == "x":
            a, b = map(int, move[1:].split("/"))
            lineup[a], lineup[b] = lineup[b], lineup[a]
        elif move[0] == "p":
            a, b = move[1:].split("/")
            ia, ib = lineup.index(a), lineup.index(b)
            lineup[ia], lineup[ib] = lineup[ib], lineup[ia]
        else:
            raise ValueError(f"Unknown move: {move}")
    return "".join(lineup)


def solve_part1(moves: List[str], programs: str = "abcdefghijklmnop") -> str:
    return dance(programs, moves)


def solve_part2(moves: List[str], programs: str = "abcdefghijklmnop", iterations: int = 1_000_000_000) -> str:
    seen: list[str] = []
    lineup = programs
    for i in range(iterations):
        if lineup in seen:
            cycle_start = seen.index(lineup)
            cycle_length = i - cycle_start
            remaining = (iterations - cycle_start) % cycle_length
            return seen[cycle_start + remaining]
        seen.append(lineup)
        lineup = dance(lineup, moves)
    return lineup


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2017 Day 16.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--programs", default="abcdefghijklmnop")
    parser.add_argument("--iterations", type=int, default=1_000_000_000)
    args = parser.parse_args()

    moves = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(moves, programs=args.programs)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(moves, programs=args.programs, iterations=args.iterations)}")


if __name__ == "__main__":
    main()
