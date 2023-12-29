#!/usr/bin/env python3
"""Lavaduct Lagoon"""
import itertools


Step = tuple[complex, int, str]


__DIRECTION = {"R": 1, "U": 1j, "L": -1, "D": -1j}


def parse_step(text: str) -> Step:
    raw_direction, distance, color = text.split()
    return __DIRECTION[raw_direction], int(distance), color[2:-1]


def read_and_parse(filename: str) -> list[Step]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(parse_step, file.read().splitlines()))


class Polygon:
    """a polygon with complex vertices"""

    def __init__(self, raw: list[complex]):
        self.raw = raw[:]

    def calculate_perimeter(self) -> float:
        return sum(abs(curr - prev) for prev, curr in itertools.pairwise(self.raw))

    def calculate_area(self) -> float:
        return abs(
            sum(
                (curr.real - prev.real) * (prev.imag + curr.imag) / 2
                for prev, curr in itertools.pairwise(self.raw)
            )
        )


def solve_part_one(plan: list[Step]) -> int:
    raw: list[complex] = [0]
    for direction, distance, _ in plan:
        raw.append(raw[-1] + distance * direction)
    polygon = Polygon(raw)
    return int(polygon.calculate_area() + polygon.calculate_perimeter() / 2 + 1)


def solve_part_two(plan: list[tuple[complex, int, str]]) -> int:
    raw: list[complex] = [0]
    for *_, raw_both in plan:
        distance = int(raw_both[:5], base=16)
        direction = __DIRECTION["RDLU"[int(raw_both[-1])]]
        raw.append(raw[-1] + distance * direction)
    polygon = Polygon(raw)
    return int(polygon.calculate_area() + polygon.calculate_perimeter() / 2 + 1)


def test():
    plan = read_and_parse("example.txt")
    part_one_answer = solve_part_one(plan)
    assert part_one_answer == 62
    part_two_answer = solve_part_two(plan)
    assert part_two_answer == 952_408_144_115


def main():
    plan = read_and_parse("input.txt")
    part_one_answer = solve_part_one(plan)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(plan)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
