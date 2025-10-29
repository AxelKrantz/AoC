from __future__ import annotations

import argparse
import os
import sys
from urllib.error import HTTPError, URLError

if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from automation import aoc_client  # type: ignore
else:
    from . import aoc_client


def store_input(year: int, day: int, contents: str, dest_root: Path) -> Path:
    dest_dir = dest_root / f"y{year}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / f"day_{day:02d}.txt"
    dest_file.write_text(contents, encoding="utf-8")
    return dest_file


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Advent of Code puzzle input.")
    parser.add_argument("year", type=int, help="Puzzle year, e.g. 2015.")
    parser.add_argument("day", type=int, help="Puzzle day number, 1-25.")
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("inputs"),
        help="Destination directory for inputs (default: inputs/).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        contents = aoc_client.fetch_input(args.year, args.day)
    except (aoc_client.AoCClientError, HTTPError, URLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    dest_file = store_input(args.year, args.day, contents, args.dest)
    print(f"Wrote puzzle input to {dest_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
