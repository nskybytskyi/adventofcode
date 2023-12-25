#!/usr/bin/env python3
"""Never Tell Me The Odds"""
import itertools
import collections


Ray = collections.namedtuple("Ray", ["x", "y", "z", "vx", "vy", "vz"])


def read_and_parse(filename: str) -> list[Ray]:
    with open(filename, "r", encoding="utf-8") as file:
        return [Ray(*map(int, line.replace(' @ ', ', ').split(', ')))
                for line in file.read().splitlines()]


def xy_intersect(fst_ray: Ray, snd_ray: Ray,
                 lower_bound: int, upper_bound: int) -> bool:
    det = fst_ray.vx * snd_ray.vy - fst_ray.vy * snd_ray.vx
    if det == 0:
        return False

    fst_time = ((snd_ray.x - fst_ray.x) * snd_ray.vy -
                (snd_ray.y - fst_ray.y) * snd_ray.vx) / det
    if fst_time < 0:
        return False

    x_coord = fst_ray.x + fst_time * fst_ray.vx
    y_coord = fst_ray.y + fst_time * fst_ray.vy
    if (x_coord - snd_ray.x) / snd_ray.vx < 0:
        return False

    return (lower_bound <= x_coord <= upper_bound and
            lower_bound <= y_coord <= upper_bound)


def solve_part_one(rays: list[Ray], lower_bound: int, upper_bound: int) -> int:
    return sum(xy_intersect(fst_ray, snd_ray, lower_bound, upper_bound)
               for fst_ray, snd_ray in itertools.combinations(rays, 2))


def solve_part_two(_) -> int:
    return 0  # TODO


def test():
    rays = read_and_parse("example.txt")
    part_one_answer = solve_part_one(rays, 7, 27)
    assert part_one_answer == 2
    # part_two_answer = solve_part_two(rays)
    # assert part_two_answer == 47


def main():
    rays = read_and_parse("input.txt")
    part_one_answer = solve_part_one(rays, 2 * 10**14, 4 * 10**14)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(rays)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
