from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


DIRECTION_VECTORS = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


TURN_LEFT = {"^": "<", "<": "v", "v": ">", ">": "^"}
TURN_RIGHT = {"^": ">", ">": "v", "v": "<", "<": "^"}


@dataclass
class Cart:
    x: int
    y: int
    direction: str
    next_turn: int = 0  # 0: left, 1: straight, 2: right
    active: bool = True

    def copy(self) -> "Cart":
        return Cart(self.x, self.y, self.direction, self.next_turn, self.active)

    def move(self) -> None:
        dx, dy = DIRECTION_VECTORS[self.direction]
        self.x += dx
        self.y += dy

    def turn(self, track_piece: str) -> None:
        if track_piece == "/":
            if self.direction in "^v":
                self.direction = TURN_RIGHT[self.direction]
            else:
                self.direction = TURN_LEFT[self.direction]
        elif track_piece == "\\":
            if self.direction in "^v":
                self.direction = TURN_LEFT[self.direction]
            else:
                self.direction = TURN_RIGHT[self.direction]
        elif track_piece == "+":
            if self.next_turn == 0:
                self.direction = TURN_LEFT[self.direction]
            elif self.next_turn == 2:
                self.direction = TURN_RIGHT[self.direction]
            self.next_turn = (self.next_turn + 1) % 3


@dataclass
class Track:
    grid: List[List[str]]
    carts: List[Cart]


def parse(raw: str) -> Track:
    grid = [list(line) for line in raw.rstrip("\n").splitlines()]
    carts: list[Cart] = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in DIRECTION_VECTORS:
                carts.append(Cart(x, y, char))
                grid[y][x] = "-" if char in "<>" else "|"
    return Track(grid=grid, carts=carts)


def simulate(track: Track, stop_on_first_collision: bool) -> tuple[int, int]:
    carts = [cart.copy() for cart in track.carts]
    width = max(len(row) for row in track.grid)
    height = len(track.grid)

    while True:
        carts.sort(key=lambda cart: (cart.y, cart.x))
        positions: dict[tuple[int, int], Cart] = {
            (cart.x, cart.y): cart for cart in carts if cart.active
        }
        collisions: list[tuple[int, int]] = []

        for cart in carts:
            if not cart.active:
                continue
            positions.pop((cart.x, cart.y), None)
            cart.move()
            if not (0 <= cart.y < height and 0 <= cart.x < len(track.grid[cart.y])):
                raise RuntimeError("Cart moved off the track.")
            track_piece = track.grid[cart.y][cart.x]
            cart.turn(track_piece)
            pos = (cart.x, cart.y)
            other = positions.get(pos)
            if other is not None and other.active:
                cart.active = False
                other.active = False
                positions.pop(pos, None)
                collisions.append(pos)
                if stop_on_first_collision:
                    return pos
            else:
                positions[pos] = cart

        if stop_on_first_collision and collisions:
            return collisions[0]

        carts = [cart for cart in carts if cart.active]
        if len(carts) == 1:
            final_cart = carts[0]
            return final_cart.x, final_cart.y


def solve_part1(track: Track) -> tuple[int, int]:
    return simulate(track, stop_on_first_collision=True)


def solve_part2(track: Track) -> tuple[int, int]:
    return simulate(track, stop_on_first_collision=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2018 Day 13.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    track = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        x, y = solve_part1(track)
        print(f"Part 1: {x},{y}")
    if args.part in {"2", "both"}:
        x, y = solve_part2(track)
        print(f"Part 2: {x},{y}")


if __name__ == "__main__":
    main()

