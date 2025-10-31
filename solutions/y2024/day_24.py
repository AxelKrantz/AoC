from __future__ import annotations

import argparse
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class Gate:
    op: str
    left: str
    right: str
    output: str


def parse(raw: str) -> tuple[Dict[str, int], list[Gate]]:
    sections = raw.strip().split("\n\n")
    wires: Dict[str, int] = {}
    gates: list[Gate] = []

    if sections:
        for line in sections[0].splitlines():
            line = line.strip()
            if not line:
                continue
            name, value = line.split(":")
            wires[name.strip()] = int(value.strip())

    if len(sections) >= 2:
        for line in sections[1].splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            left, op, right, _, output = parts
            gates.append(Gate(op, left, right, output))

    return wires, gates


def topological_order(gates: Sequence[Gate], initial_wires: Sequence[str]) -> list[Gate]:
    produced_by: Dict[str, Gate] = {gate.output: gate for gate in gates}
    initial_set = set(initial_wires)
    indegree: Dict[Gate, int] = {}
    dependents: Dict[str, list[Gate]] = {}

    for gate in gates:
        dependencies = 0
        for wire in (gate.left, gate.right):
            if wire in produced_by:
                dependencies += 1
                dependents.setdefault(wire, []).append(gate)
        indegree[gate] = dependencies

    queue = deque([gate for gate in gates if indegree[gate] == 0])
    order: list[Gate] = []

    while queue:
        gate = queue.popleft()
        order.append(gate)
        output_wire = gate.output
        for dependent in dependents.get(output_wire, []):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(gates):
        raise ValueError("Cycle detected in gate configuration.")

    return order


def evaluate(
    base_values: Dict[str, int],
    gates: Sequence[Gate],
    gate_order: Sequence[Gate],
    output_remap: Dict[str, str] | None = None,
    overrides: Dict[str, int] | None = None,
) -> Dict[str, int]:
    values: Dict[str, int] = dict(base_values)
    if overrides:
        values.update(overrides)

    remap = output_remap or {}

    for gate in gate_order:
        left = values.get(gate.left)
        right = values.get(gate.right)
        if left is None or right is None:
            raise KeyError(f"Input wires {gate.left} or {gate.right} missing value.")

        if gate.op == "AND":
            result = left & right
        elif gate.op == "OR":
            result = left | right
        elif gate.op == "XOR":
            result = left ^ right
        else:
            raise ValueError(f"Unsupported operation {gate.op}")

        output = remap.get(gate.output, gate.output)
        values[output] = result

    return values


def z_value(values: Dict[str, int]) -> int:
    z_bits = sorted([wire for wire in values if wire.startswith("z")])
    total = 0
    for idx, wire in enumerate(z_bits):
        bit = values.get(wire, 0)
        total |= (bit & 1) << idx
    return total


def solve_part1(raw: str) -> int:
    base_values, gates = parse(raw)
    order = topological_order(gates, base_values.keys())
    values = evaluate(base_values, gates, order)
    return z_value(values)


def deduce_swaps(base_values: Dict[str, int], gates: Sequence[Gate]) -> tuple[list[tuple[str, str]], Dict[str, str]]:
    by_inputs: Dict[tuple[str, frozenset[str]], list[str]] = {}
    uses: Dict[str, list[Gate]] = defaultdict(list)
    for gate in gates:
        key = (gate.op, frozenset({gate.left, gate.right}))
        by_inputs.setdefault(key, []).append(gate.output)
        uses[gate.left].append(gate)
        uses[gate.right].append(gate)

    x_bits = sorted([wire for wire in base_values if wire.startswith("x")])
    bits = len(x_bits)

    partial: Dict[int, str] = {}
    and_xy: Dict[int, str] = {}
    for i in range(bits):
        key_xor = ("XOR", frozenset({f"x{i:02d}", f"y{i:02d}"}))
        key_and = ("AND", frozenset({f"x{i:02d}", f"y{i:02d}"}))
        partial[i] = by_inputs[key_xor][0]
        and_xy[i] = by_inputs[key_and][0]

    source_to_wire: Dict[str, str] = {gate.output: gate.output for gate in gates}
    wire_to_source: Dict[str, str] = {gate.output: gate.output for gate in gates}
    for wire in base_values:
        source_to_wire.setdefault(wire, wire)
        wire_to_source.setdefault(wire, wire)

    swaps: list[tuple[str, str]] = []

    def perform_swap(wire_a: str, wire_b: str) -> None:
        if wire_a == wire_b:
            return
        src_a = wire_to_source[wire_a]
        src_b = wire_to_source[wire_b]
        wire_to_source[wire_a], wire_to_source[wire_b] = src_b, src_a
        source_to_wire[src_a], source_to_wire[src_b] = wire_b, wire_a
        swaps.append(tuple(sorted((wire_a, wire_b))))

    carry_source = and_xy[0]
    for i in range(1, bits):
        while True:
            partial_wire = source_to_wire[partial[i]]
            carry_wire = source_to_wire[carry_source]
            key = ("XOR", frozenset({partial_wire, carry_wire}))
            xor_sources = by_inputs.get(key)
            if xor_sources:
                xor_source = xor_sources[0]
                xor_wire = source_to_wire[xor_source]
                expected_wire = f"z{i:02d}"
                if xor_wire != expected_wire:
                    perform_swap(xor_wire, expected_wire)
                    continue
            else:
                candidates = [gate for gate in uses[carry_wire] if gate.op == "XOR"]
                if len(candidates) != 1:
                    raise ValueError(f"Unable to resolve XOR gate for bit {i}")
                gate = candidates[0]
                other_wire = gate.left if gate.right == carry_wire else gate.right
                perform_swap(partial_wire, other_wire)
                continue
            break

        partial_wire = source_to_wire[partial[i]]
        carry_wire = source_to_wire[carry_source]
        and_key = ("AND", frozenset({partial_wire, carry_wire}))
        and_source = by_inputs[and_key][0]
        and_wire = source_to_wire[and_source]

        while True:
            left_wire = source_to_wire[and_xy[i]]
            or_key = ("OR", frozenset({left_wire, and_wire}))
            or_sources = by_inputs.get(or_key)
            if or_sources:
                carry_source = or_sources[0]
                break
            candidates = [
                gate
                for gate in uses[left_wire]
                if gate.op == "OR" and (gate.left == and_wire or gate.right == and_wire)
            ]
            if len(candidates) != 1:
                raise ValueError(f"Unable to resolve OR gate for bit {i}")
            perform_swap(left_wire, candidates[0].output)

    output_remap = {source: wire for source, wire in source_to_wire.items() if source != wire}
    unique_swaps = sorted(set(swaps))
    return unique_swaps, output_remap


def solve_part2(raw: str) -> str:
    base_values, gates = parse(raw)
    swap_pairs, output_remap = deduce_swaps(base_values, gates)

    # Optional verification: ensure circuit now behaves as adder for random samples.
    order = topological_order(gates, base_values.keys())
    x_wires = sorted([wire for wire in base_values if wire.startswith("x")])
    y_wires = sorted([wire for wire in base_values if wire.startswith("y")])

    import random

    for _ in range(40):
        x = random.randrange(1 << len(x_wires))
        y = random.randrange(1 << len(y_wires))
        overrides = {wire: (x >> idx) & 1 for idx, wire in enumerate(x_wires)}
        overrides.update({wire: (y >> idx) & 1 for idx, wire in enumerate(y_wires)})
        values = evaluate(base_values, gates, order, output_remap=output_remap, overrides=overrides)
        expected = x + y
        if z_value(values) != expected:
            raise RuntimeError("Swap deduction verification failed.")

    wires = sorted({wire for pair in swap_pairs for wire in pair})
    return ",".join(wires)


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve Advent of Code 2024 Day 24.")
    parser.add_argument("input_path", type=Path, help="Path to the puzzle input file.")
    parser.add_argument("--part", choices={"1", "2"}, default="1")
    args = parser.parse_args()

    raw = args.input_path.read_text(encoding="utf-8")
    if args.part == "1":
        result = solve_part1(raw)
    else:
        result = solve_part2(raw)
    print(result)


if __name__ == "__main__":
    main()
