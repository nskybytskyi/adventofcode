#!/usr/bin/env python3
"""Point of Incidence"""
import functools
from typing import Iterable


def read_and_parse(filename: str) -> list[list[str]]:
    """gridlike mirrors separated by empty lines"""
    with open(filename, "r", encoding="utf-8") as file:
        return [grid.split("\n") for grid in file.read().split("\n\n")]


def custom_hash(text: Iterable[str]) -> int:
    return functools.reduce(lambda acc, char: (acc << 1) | (char == "#"), text, 0)


def find_row(grid: Iterable[Iterable[str]], smudge: int) -> int:
    hashes = list(map(custom_hash, grid))

    def is_mirror(middle: int) -> bool:
        return smudge == sum(
            (x ^ y).bit_count()
            for x, y in zip(reversed(hashes[:middle]), hashes[middle:])
        )

    return next(filter(is_mirror, range(1, len(hashes))), 0)


def find_reflection(grid: list[str], smudge: int) -> int:
    """locate the mirror with a potential smudge"""
    return 100 * find_row(grid, smudge) or find_row(zip(*grid), smudge)


def solve_part_one(grids: list[list[str]]) -> int:
    """summary of notes without smudges"""
    return sum(find_reflection(grid, 0) for grid in grids)


def solve_part_two(grids: list[list[str]]) -> int:
    """summary of notes with smudges"""
    return sum(find_reflection(grid, 1) for grid in grids)


def test():
    grids = read_and_parse("example.txt")
    part_one_answer = solve_part_one(grids)
    assert part_one_answer == 405
    part_two_answer = solve_part_two(grids)
    assert part_two_answer == 400


def main():
    grids = read_and_parse("input.txt")
    part_one_answer = solve_part_one(grids)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(grids)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
