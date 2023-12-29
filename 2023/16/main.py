#!/usr/bin/env python3
"""The Floor Will Be Lava"""
import collections
from typing import Iterable


class Grid:
    """2d grid with complex indexing"""

    def __init__(self, raw: list[str]):
        self.raw = raw[:]

    def shape(self) -> tuple[int, int]:
        return len(self.raw), len(self.raw[0])

    def __contains__(self, cell: complex) -> bool:
        row, col = int(cell.real), int(cell.imag)
        return 0 <= row < len(self.raw) and 0 <= col < len(self.raw[0])

    def __getitem__(self, cell: complex) -> str:
        return self.raw[int(cell.real)][int(cell.imag)]

    def find_neighbors(
        self, location: complex, direction: complex
    ) -> Iterable[tuple[complex, complex]]:
        if self[location] == "|" and direction.imag:
            yield location + 1, 1
            yield location - 1, -1
        elif self[location] == "-" and direction.real:
            yield location + 1j, 1j
            yield location - 1j, -1j
        elif self[location] == "\\":
            direction = direction.imag + direction.real * 1j
            yield location + direction, direction
        elif self[location] == "/":
            direction = direction.imag + direction.real * 1j
            yield location - direction, -direction
        else:
            yield location + direction, direction


def breadth_first_search(grid: Grid, start: tuple[complex, complex]) -> int:
    seen = {start}
    queue = collections.deque([start])

    while queue:
        for node in grid.find_neighbors(*queue.popleft()):
            if node[0] in grid and node not in seen:
                seen.add(node)
                queue.append(node)

    return len({location for location, _ in seen})


def read_and_parse(filename: str) -> Grid:
    with open(filename, "r", encoding="utf-8") as file:
        return Grid(file.read().splitlines())


def solve_part_one(grid: Grid) -> int:
    return breadth_first_search(grid, (0, 1j))


def solve_part_two(grid: Grid) -> int:
    rows, cols = grid.shape()
    candidates = (
        [(row, 1j) for row in range(rows)]
        + [(row + (cols - 1) * 1j, -1j) for row in range(rows)]
        + [(col * 1j, 1) for col in range(cols)]
        + [(rows - 1 + col * 1j, -1) for col in range(cols)]
    )
    return max(breadth_first_search(grid, candidate) for candidate in candidates)


def test():
    grid = read_and_parse("example.txt")
    part_one_answer = solve_part_one(grid)
    assert part_one_answer == 46
    part_two_answer = solve_part_two(grid)
    assert part_two_answer == 51


def main():
    grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
