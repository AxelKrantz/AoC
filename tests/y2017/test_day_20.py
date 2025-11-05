from solutions.y2017 import day_20


PART1_SAMPLE = """\
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
"""


PART2_SAMPLE = """\
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>
"""


def test_particle_swarm_closest_example() -> None:
    particles = day_20.parse(PART1_SAMPLE)
    assert day_20.solve_part1(particles) == 0


def test_particle_swarm_collisions_example() -> None:
    particles = day_20.parse(PART2_SAMPLE)
    assert day_20.solve_part2(particles) == 1
