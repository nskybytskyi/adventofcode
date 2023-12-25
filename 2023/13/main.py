#!/usr/bin/env python3
"""Point of Incidence"""


def read_and_parse(filename: str) -> list[list[str]]:
    """gridlike mirrors separated by empty lines"""
    with open(filename, "r", encoding="utf-8") as file:
        return [grid.split('\n') for grid in file.read().split('\n\n')]


def find_reflection(grid: list[str], smudge: int) -> int:
    """locate the mirror with a potential smudge"""
    rows, cols = len(grid), len(grid[0])

    for middle in range(1, rows):
        count = 0

        for shift in range(min(middle, rows - middle)):
            top, bottom = middle - 1 - shift, middle + shift
            for col in range(cols):
                count += grid[top][col] != grid[bottom][col]

        if count == smudge:
            return 100 * middle

    for middle in range(1, cols):
        count = 0

        for shift in range(min(middle, cols - middle)):
            left, right = middle - 1 - shift, middle + shift
            for row in range(rows):
                count += grid[row][left] != grid[row][right]

        if count == smudge:
            return middle

    assert False


def solve_part_one(mirrors: list[list[str]]) -> int:
    """summary of notes without smudges"""
    return sum(find_reflection(grid, 0) for grid in mirrors)


def solve_part_two(mirrors: list[list[str]]) -> int:
    """summary of notes with smudges"""
    return sum(find_reflection(grid, 1) for grid in mirrors)


def test():
    mirrors = read_and_parse("example.txt")
    part_one_answer = solve_part_one(mirrors)
    assert part_one_answer == 405
    part_two_answer = solve_part_two(mirrors)
    assert part_two_answer == 400


def main():
    mirrors = read_and_parse("input.txt")
    part_one_answer = solve_part_one(mirrors)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(mirrors)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
