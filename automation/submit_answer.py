from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import dedent
from urllib.error import HTTPError, URLError

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from automation import aoc_client  # type: ignore
else:
    from . import aoc_client


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit an Advent of Code answer.")
    parser.add_argument("year", type=int, help="Puzzle year, e.g. 2015.")
    parser.add_argument("day", type=int, help="Puzzle day number, 1-25.")
    parser.add_argument("part", type=int, choices=(1, 2), help="Puzzle part to submit (1 or 2).")
    parser.add_argument(
        "answer",
        type=str,
        help="Computed answer to submit. For numbers, pass them exactly as AoC expects.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the submission payload without sending it.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional file to store the raw HTML response for auditing.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.dry_run:
        print(
            dedent(
                f"""
                Dry run enabled. Would submit:
                  year={args.year}
                  day={args.day}
                  part={args.part}
                  answer={args.answer}
                """
            ).strip()
        )
        return 0

    try:
        html = aoc_client.submit_answer(args.year, args.day, args.part, args.answer)
    except (aoc_client.AoCClientError, HTTPError, URLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.out:
        args.out.write_text(html, encoding="utf-8")
        print(f"Wrote response to {args.out}")
    else:
        print(html.splitlines()[0].strip())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
