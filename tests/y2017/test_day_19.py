from solutions.y2017 import day_19


SAMPLE = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
"""


def test_series_of_tubes_example() -> None:
    diagram = day_19.parse(SAMPLE)
    assert day_19.solve_part1(diagram) == "ABCDEF"
    assert day_19.solve_part2(diagram) == 38
