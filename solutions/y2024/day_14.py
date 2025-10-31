from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import Iterable, Iterator


@dataclass(frozen=True)
class Robot:
    x: int
    y: int
    vx: int
    vy: int


def parse(raw: str) -> list[Robot]:
    robots: list[Robot] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        left, right = line.split()
        x_str, y_str = left.split("=")[1].split(",")
        vx_str, vy_str = right.split("=")[1].split(",")
        robots.append(
            Robot(
                x=int(x_str),
                y=int(y_str),
                vx=int(vx_str),
                vy=int(vy_str),
            )
        )
    return robots


def move(robot: Robot, seconds: int, width: int, height: int) -> Robot:
    new_x = (robot.x + robot.vx * seconds) % width
    new_y = (robot.y + robot.vy * seconds) % height
    return Robot(new_x, new_y, robot.vx, robot.vy)


def positions_at(robots: Iterable[Robot], seconds: int, width: int, height: int) -> list[Robot]:
    return [move(robot, seconds, width, height) for robot in robots]


def safety_factor(robots: Iterable[Robot], width: int, height: int) -> int:
    robots_by_quadrant = [0, 0, 0, 0]
    midpoint_x = width // 2
    midpoint_y = height // 2

    for robot in robots:
        if robot.x == midpoint_x or robot.y == midpoint_y:
            continue
        index = 0
        if robot.x > midpoint_x:
            index += 1
        if robot.y > midpoint_y:
            index += 2
        robots_by_quadrant[index] += 1

    return prod(robots_by_quadrant)


def solve_part1(robots: Iterable[Robot], width: int, height: int) -> int:
    positions = positions_at(robots, 100, width, height)
    return safety_factor(positions, width, height)


def bounding_box_area(robots: Iterable[Robot]) -> int:
    xs = [robot.x for robot in robots]
    ys = [robot.y for robot in robots]
    return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)


def adjacency_score(robots: Iterable[Robot]) -> int:
    points = {(robot.x, robot.y) for robot in robots}
    score = 0
    for x, y in points:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) in points:
                score += 1
    return score


def max_horizontal_run(robots: Iterable[Robot]) -> int:
    rows: dict[int, list[int]] = {}
    for robot in robots:
        rows.setdefault(robot.y, []).append(robot.x)
    longest = 0
    for cols in rows.values():
        cols.sort()
        current = 1
        for i in range(1, len(cols)):
            if cols[i] == cols[i - 1] + 1:
                current += 1
            else:
                longest = max(longest, current)
                current = 1
        longest = max(longest, current)
    return longest


def solve_part2(robots: Iterable[Robot], width: int, height: int) -> tuple[int, list[Robot]]:
    period = width * height
    best_seconds = 0
    best_state = positions_at(robots, 0, width, height)
    best_area = bounding_box_area(best_state)
    best_adj = adjacency_score(best_state)
    best_run = max_horizontal_run(best_state)
    for seconds in range(1, period + 1):
        state = positions_at(robots, seconds, width, height)
        area = bounding_box_area(state)
        adj = adjacency_score(state)
        run = max_horizontal_run(state)
        if run > best_run:
            best_run = run
            best_adj = adj
            best_area = area
            best_seconds = seconds
            best_state = state
        elif run == best_run:
            if adj > best_adj:
                best_adj = adj
                best_area = area
                best_seconds = seconds
                best_state = state
            elif adj == best_adj and area < best_area:
                best_area = area
                best_seconds = seconds
                best_state = state
    return best_seconds, best_state


def render(robots: Iterable[Robot], width: int, height: int) -> str:
    grid = [["." for _ in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot.y][robot.x] = "#"
    return "\n".join("".join(row) for row in grid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 14.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--width", type=int, default=101)
    parser.add_argument("--height", type=int, default=103)
    parser.add_argument("--part", choices={"1", "2", "both"}, default="both")
    args = parser.parse_args()

    robots = parse(args.input_path.read_text(encoding="utf-8"))

    if args.part in {"1", "both"}:
        print(f"Part 1: {solve_part1(robots, args.width, args.height)}")
    if args.part in {"2", "both"}:
        seconds, state = solve_part2(robots, args.width, args.height)
        print(f"Part 2: {seconds}")
        print(render(state, args.width, args.height))


if __name__ == "__main__":
    main()
