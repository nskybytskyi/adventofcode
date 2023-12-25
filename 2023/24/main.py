#!/usr/bin/env python3
"""Never Tell Me The Odds"""
import itertools


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return [list(map(int, line.replace(' @ ', ', ').split(', ')))
                for line in file.read().splitlines()]


def xy_intersect(a1, a2, mn, mx):
    x1, y1, _, vx1, vy1, _ = a1
    x2, y2, _, vx2, vy2, _ = a2

    det = vx1 * vy2 - vy1 * vx2
    if det == 0:
        return False

    t1 = ((x2 - x1) * vy2 - (y2 - y1) * vx2) / det
    if t1 < 0:
        return False

    x, y = (x1 + t1 * vx1, y1 + t1 * vy1)
    if (x - x2) / vx2 < 0:
        return False
    
    return mn <= x <= mx and mn <= y <= mx


def solve_part_one(a, mn, mx) -> int:
    return sum(xy_intersect(a1, a2, mn, mx)
               for a1, a2 in itertools.combinations(a, 2))


def solve_part_two(a) -> str:
    pass


def test():
    a = read_and_parse("example.txt")
    part_one_answer = solve_part_one(a, 7, 27)
    assert part_one_answer == 2
    part_two_answer = solve_part_two(a)
    assert part_two_answer == 47


def main():
    a = read_and_parse("input.txt")
    part_one_answer = solve_part_one(a, 200_000_000_000_000, 400_000_000_000_000)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(a)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
