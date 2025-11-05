from __future__ import annotations

import argparse
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, Dict, List, Tuple


@dataclass(frozen=True)
class ValueInstruction:
    value: int
    bot: int


@dataclass(frozen=True)
class BotInstruction:
    bot: int
    low_target: tuple[str, int]
    high_target: tuple[str, int]


def parse(raw: str) -> tuple[list[ValueInstruction], dict[int, BotInstruction]]:
    values: list[ValueInstruction] = []
    bots: dict[int, BotInstruction] = {}
    for line in raw.strip().splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "value":
            value = int(parts[1])
            bot = int(parts[-1])
            values.append(ValueInstruction(value=value, bot=bot))
        elif parts[0] == "bot":
            bot = int(parts[1])
            low_type = parts[5]
            low_id = int(parts[6])
            high_type = parts[10]
            high_id = int(parts[11])
            bots[bot] = BotInstruction(
                bot=bot,
                low_target=(low_type, low_id),
                high_target=(high_type, high_id),
            )
        else:
            raise ValueError(f"Unknown instruction: {line}")
    return values, bots


def run_factory(
    values: List[ValueInstruction],
    bot_instructions: Dict[int, BotInstruction],
    target_low: int = 17,
    target_high: int = 61,
) -> tuple[int | None, Dict[int, int]]:
    bots: dict[int, list[int]] = defaultdict(list)
    outputs: dict[int, int] = {}
    queue: Deque[int] = deque()
    comparer_bot: int | None = None

    def enqueue(bot_id: int) -> None:
        if len(bots[bot_id]) == 2:
            queue.append(bot_id)

    for instruction in values:
        bots[instruction.bot].append(instruction.value)
        enqueue(instruction.bot)

    while queue:
        bot_id = queue.popleft()
        chips = bots[bot_id]
        if len(chips) < 2:
            continue
        low, high = sorted(chips)
        if low == target_low and high == target_high:
            comparer_bot = bot_id
        bots[bot_id] = []
        instruction = bot_instructions.get(bot_id)
        if instruction is None:
            continue

        for value, target in [(low, instruction.low_target), (high, instruction.high_target)]:
            target_type, target_id = target
            if target_type == "bot":
                bots[target_id].append(value)
                enqueue(target_id)
            elif target_type == "output":
                outputs[target_id] = value
            else:
                raise ValueError(f"Unknown target type: {target_type}")

    return comparer_bot, outputs


def solve_part1(
    values: List[ValueInstruction],
    bot_instructions: Dict[int, BotInstruction],
    target_low: int = 17,
    target_high: int = 61,
) -> int:
    comparer, _ = run_factory(values, bot_instructions, target_low=target_low, target_high=target_high)
    if comparer is None:
        raise ValueError("Target comparison bot not found.")
    return comparer


def solve_part2(values: List[ValueInstruction], bot_instructions: Dict[int, BotInstruction]) -> int:
    _, outputs = run_factory(values, bot_instructions)
    return outputs.get(0, 1) * outputs.get(1, 1) * outputs.get(2, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2016 Day 10.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    parser.add_argument("--target-low", type=int, default=17)
    parser.add_argument("--target-high", type=int, default=61)
    args = parser.parse_args()

    values, bots = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        result = solve_part1(values, bots, target_low=args.target_low, target_high=args.target_high)
        print(f"Part 1: {result}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(values, bots)}")


if __name__ == "__main__":
    main()
