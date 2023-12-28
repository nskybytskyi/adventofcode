#!/usr/bin/env python3
"""Parabolic Reflector Dish"""
import copy


class Grid:
    def __init__(self, raw: list[str]):
        self.raw = raw[:]

    def __eq__(self, other) -> bool:
        return self.raw == other.raw

    def tilt_left(self):
        self.raw = [
            "#".join("".join(sorted(group, reverse=True)) for group in row.split("#"))
            for row in self.raw
        ]

    def transpose(self):
        self.raw = list(map("".join, zip(*self.raw)))

    def reverse_rows(self):
        self.raw = [row[::-1] for row in self.raw]

    def calculate_load(self) -> int:
        return sum(
            distance * row.count("O")
            for distance, row in enumerate(reversed(self.raw), start=1)
        )


def read_and_parse(filename: str) -> Grid:
    with open(filename, "r", encoding="utf-8") as file:
        return Grid(file.read().splitlines())


def solve_part_one(grid: Grid) -> int:
    grid = copy.deepcopy(grid)
    grid.transpose()
    grid.tilt_left()
    grid.transpose()
    return grid.calculate_load()


def solve_part_two(grid: Grid) -> int:
    grid = copy.deepcopy(grid)

    seen = []
    while grid not in seen:
        seen.append(copy.deepcopy(grid))

        for _ in range(4):
            grid.transpose()
            grid.tilt_left()
            grid.reverse_rows()

    offset = seen.index(grid)
    final = seen[offset + ((10**9 - offset) % (len(seen) - offset))]
    return final.calculate_load()


def test():
    grid = read_and_parse("example.txt")
    part_one_answer = solve_part_one(grid)
    assert part_one_answer == 136
    part_two_answer = solve_part_two(grid)
    assert part_two_answer == 64


def main():
    grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
