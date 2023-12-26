#!/usr/bin/env python3
"""Gear Ratios"""
import math
import re
from typing import Iterable


Cell = tuple[int, int]
Segment = tuple[int, int, int]


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def find_symbols_in_grid(
    grid: list[str], symbols: str = "#$%&*+-/=@"
) -> Iterable[Cell]:
    return (
        (i, j)
        for i, row in enumerate(grid)
        for j, char in enumerate(row)
        if char in symbols
    )


def find_numbers_in_grid(grid: list[str]) -> Iterable[Segment]:
    return (
        (i, n.start(), n.end())
        for i, row in enumerate(grid)
        for n in re.finditer(r"\d+", row)
    )


def find_adjacent_pairs(grid: list[str]) -> dict[Cell, list[int]]:
    pairs = {symbol: [] for symbol in find_symbols_in_grid(grid)}

    for row, start, end in find_numbers_in_grid(grid):
        edge = {
            (row, col)
            for row in (row - 1, row, row + 1)
            for col in range(start - 1, end + 1)
        }

        for symbol in edge & pairs.keys():
            pairs[symbol].append(int(grid[row][start:end]))

    return pairs


def solve_part_one(engine_schematic: list[str]) -> int:
    pairs = find_adjacent_pairs(engine_schematic)
    return sum(map(sum, pairs.values()))


def solve_part_two(engine_schematic: list[str]) -> int:
    pairs = find_adjacent_pairs(engine_schematic)
    return sum(
        math.prod(nums)
        for (row, col), nums in pairs.items()
        if engine_schematic[row][col] == "*" and len(nums) == 2
    )


def test():
    engine_schematic = read_and_parse("example.txt")
    part_one_answer = solve_part_one(engine_schematic)
    assert part_one_answer == 4_361
    part_two_answer = solve_part_two(engine_schematic)
    assert part_two_answer == 467_835


def main():
    engine_schematic = read_and_parse("input.txt")
    part_one_answer = solve_part_one(engine_schematic)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(engine_schematic)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
