from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


RECORD_PATTERN = re.compile(
    r"\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+)\] (?P<action>.+)"
)
GUARD_PATTERN = re.compile(r"Guard #(?P<guard_id>\d+) begins shift")


def parse(raw: str) -> list[tuple[datetime, str]]:
    records: list[tuple[datetime, str]] = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = RECORD_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"Unable to parse record: {line!r}")
        timestamp = datetime(
            year=int(match.group("year")),
            month=int(match.group("month")),
            day=int(match.group("day")),
            hour=int(match.group("hour")),
            minute=int(match.group("minute")),
        )
        records.append((timestamp, match.group("action")))
    records.sort(key=lambda entry: entry[0])
    return records


def build_sleep_map(records: Iterable[tuple[datetime, str]]) -> dict[int, Counter[int]]:
    sleep_map: dict[int, Counter[int]] = defaultdict(Counter)
    current_guard: int | None = None
    asleep_minute: int | None = None

    for timestamp, action in records:
        guard_match = GUARD_PATTERN.fullmatch(action)
        if guard_match:
            current_guard = int(guard_match.group("guard_id"))
            asleep_minute = None
            continue

        if action == "falls asleep":
            asleep_minute = timestamp.minute
            continue

        if action == "wakes up":
            if current_guard is None or asleep_minute is None:
                raise RuntimeError("Encountered wake event without guard asleep.")
            for minute in range(asleep_minute, timestamp.minute):
                sleep_map[current_guard][minute] += 1
            asleep_minute = None
            continue

        raise RuntimeError(f"Unknown action: {action!r}")

    return sleep_map


def solve_part1(records: Sequence[tuple[datetime, str]]) -> int:
    sleep_map = build_sleep_map(records)
    guard_id, minutes = max(
        sleep_map.items(),
        key=lambda item: sum(item[1].values()),
    )
    minute, _ = max(minutes.items(), key=lambda item: item[1])
    return guard_id * minute


def solve_part2(records: Sequence[tuple[datetime, str]]) -> int:
    sleep_map = build_sleep_map(records)
    best_guard = 0
    best_minute = 0
    best_count = -1
    for guard_id, counts in sleep_map.items():
        if not counts:
            continue
        minute, count = max(counts.items(), key=lambda item: item[1])
        if count > best_count:
            best_guard = guard_id
            best_minute = minute
            best_count = count
    if best_count < 0:
        raise RuntimeError("No sleep records available.")
    return best_guard * best_minute


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 4.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    records = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(records)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(records)}")


if __name__ == "__main__":
    main()

