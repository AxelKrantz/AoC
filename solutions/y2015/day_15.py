from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


@dataclass(frozen=True)
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


PROPERTIES = ("capacity", "durability", "flavor", "texture")


def parse(raw: str) -> list[Ingredient]:
    ingredients: list[Ingredient] = []
    for line in raw.strip().splitlines():
        name, rest = line.split(": ")
        values: dict[str, int] = {}
        for part in rest.split(", "):
            prop, value = part.split()
            values[prop] = int(value)
        ingredients.append(
            Ingredient(
                name=name,
                capacity=values["capacity"],
                durability=values["durability"],
                flavor=values["flavor"],
                texture=values["texture"],
                calories=values["calories"],
            )
        )
    return ingredients


def distributions(total: int, count: int) -> Iterator[tuple[int, ...]]:
    if count == 1:
        yield (total,)
        return
    for amount in range(total + 1):
        for rest in distributions(total - amount, count - 1):
            yield (amount,) + rest


def best_score(ingredients: list[Ingredient], *, calorie_target: int | None) -> int:
    highest = 0
    for amounts in distributions(100, len(ingredients)):
        result, calories = score_with_calories(ingredients, amounts)
        if calorie_target is not None and calories != calorie_target:
            continue
        highest = max(highest, result)
    return highest


def score_with_calories(
    ingredients: list[Ingredient], amounts: Iterable[int]
) -> tuple[int, int]:
    totals = {prop: 0 for prop in PROPERTIES}
    calories = 0
    for ingredient, amount in zip(ingredients, amounts):
        totals["capacity"] += ingredient.capacity * amount
        totals["durability"] += ingredient.durability * amount
        totals["flavor"] += ingredient.flavor * amount
        totals["texture"] += ingredient.texture * amount
        calories += ingredient.calories * amount
    if any(value <= 0 for value in totals.values()):
        return 0, calories
    product = 1
    for value in totals.values():
        product *= value
    return product, calories


def solve_part1(ingredients: list[Ingredient]) -> int:
    return best_score(ingredients, calorie_target=None)


def solve_part2(ingredients: list[Ingredient]) -> int:
    return best_score(ingredients, calorie_target=500)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2015 Day 15.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    ingredients = parse(raw)

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(ingredients)}")
    if args.part in {"2", "both"}:
        print(f"Part 2: {solve_part2(ingredients)}")


if __name__ == "__main__":
    main()
