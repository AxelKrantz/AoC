from __future__ import annotations

import argparse
from pathlib import Path
import re
from collections import deque
from typing import Sequence, Tuple

GAME_PATTERN = re.compile(
    r"(?P<players>\d+) players; last marble is worth (?P<marble>\d+) points"
)


def parse(raw: str) -> tuple[int, int]:
    line = raw.strip()
    match = GAME_PATTERN.fullmatch(line)
    if match is None:
        raise ValueError(f"Unable to parse game description: {line!r}")
    return int(match.group("players")), int(match.group("marble"))


def play_game(players: int, last_marble: int) -> int:
    scores = [0] * players
    circle = deque([0])
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores)


def solve_part1(game: tuple[int, int]) -> int:
    players, last_marble = game
    return play_game(players, last_marble)


def solve_part2(game: tuple[int, int]) -> int:
    players, last_marble = game
    return play_game(players, last_marble * 100)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 9.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    game = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(game)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(game)}")


if __name__ == "__main__":
    main()
