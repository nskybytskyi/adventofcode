#!/usr/bin/env python3
"""Pipe Maze"""
import itertools
from typing import Iterable


class Grid:
    """2d pipe grid with complex indexing"""

    __START = "S"

    __DIRECTIONS = {
        ".": [],
        "|": [1, -1],
        "-": [1j, -1j],
        "L": [1j, -1],
        "J": [-1, -1j],
        "7": [-1j, 1],
        "F": [1j, 1],
        __START: [1, 1j, -1, -1j],
    }

    def __init__(self, raw: list[str]):
        self.raw = raw[:]

    def __contains__(self, cell: complex) -> bool:
        row, col = int(cell.real), int(cell.imag)
        return 0 <= row < len(self.raw) and 0 <= col < len(self.raw[row])

    def __getitem__(self, cell: complex) -> str:
        return self.raw[int(cell.real)][int(cell.imag)]

    def index(self, target: str) -> complex:
        for i, row in enumerate(self.raw):
            for j, char in enumerate(row):
                if char == target:
                    return i + j * 1j
        assert False

    def find_neighbors(self, cell: complex) -> Iterable[complex]:
        for direction in Grid.__DIRECTIONS[self[cell]]:
            if (
                (candidate := cell + direction) in self
                and self[candidate] != "#"
                and (
                    self[cell] != Grid.__START or cell in self.find_neighbors(candidate)
                )
            ):
                yield candidate

    def find_closed_path(self, start: str = __START) -> list[complex]:
        path = [self.index(start)]

        while len(path) < 2 or path[-1] != path[0]:
            path.append(
                next(
                    cell
                    for cell in self.find_neighbors(path[-1])
                    if len(path) < 2 or cell != path[-2]
                )
            )

        return path


def read_and_parse(filename: str) -> Grid:
    with open(filename, "r", encoding="utf-8") as file:
        return Grid(file.read().splitlines())


def solve_part_one(grid: Grid) -> int:
    return len(grid.find_closed_path()) // 2


def calculate_polygon_area(polygon: list[complex]) -> float:
    return abs(
        sum(
            (curr.real - prev.real) * (prev.imag + curr.imag) / 2
            for prev, curr in itertools.pairwise(polygon)
        )
    )


def solve_part_two(grid: Grid) -> int:
    polygon = grid.find_closed_path()
    area = calculate_polygon_area(polygon)
    return int(area + 1 - (len(polygon) - 1) / 2)


def test():
    pipe_grid = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(pipe_grid)
    assert part_one_answer == 4
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 1

    pipe_grid = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 4

    pipe_grid = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 4

    pipe_grid = read_and_parse("example-4.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 4

    pipe_grid = read_and_parse("example-5.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 8

    pipe_grid = read_and_parse("example-6.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 10


def main():
    pipe_grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(pipe_grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(pipe_grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
