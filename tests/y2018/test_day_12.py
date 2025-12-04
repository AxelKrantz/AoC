from textwrap import dedent

from solutions.y2018 import day_12


EXAMPLE_INPUT = dedent(
    """\
    initial state: #..#.#..##......###...###

    ...## => #
    ..#.. => #
    .#... => #
    .#.#. => #
    .#.## => #
    .##.. => #
    .#### => #
    #.#.# => #
    #.### => #
    ##.#. => #
    ##.## => #
    ###.. => #
    ###.# => #
    ####. => #
    """
)


def test_part1_example() -> None:
    notes = day_12.parse(EXAMPLE_INPUT)
    assert day_12.solve_part1(notes) == 325


def test_part2_matches_simulation_for_smaller_target() -> None:
    notes = day_12.parse(EXAMPLE_INPUT)
    generations = 200
    expected = day_12.simulate(notes, generations)
    assert day_12.solve_part2(notes, generations=generations) == expected

