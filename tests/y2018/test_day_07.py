from solutions.y2018 import day_07


EXAMPLE_INPUT = "\n".join(
    [
        "Step C must be finished before step A can begin.",
        "Step C must be finished before step F can begin.",
        "Step A must be finished before step B can begin.",
        "Step A must be finished before step D can begin.",
        "Step B must be finished before step E can begin.",
        "Step D must be finished before step E can begin.",
        "Step F must be finished before step E can begin.",
    ]
)


def test_part1_example() -> None:
    edges = day_07.parse(EXAMPLE_INPUT)
    assert day_07.solve_part1(edges) == "CABDFE"


def test_part2_example() -> None:
    edges = day_07.parse(EXAMPLE_INPUT)
    assert day_07.solve_part2(edges, worker_count=2, base_duration=0) == 15

