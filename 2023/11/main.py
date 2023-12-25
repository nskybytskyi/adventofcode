#!/usr/bin/env python3
"""Cosmic Expansion"""


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def find_rows(grid: list[str], expansion_factor: int) -> list[int]:
    rows = []
    expanded_row = 0

    for row in grid:
        if "#" in row:
            expanded_row += 1
            rows.extend([expanded_row] * row.count("#"))
        else:
            expanded_row += expansion_factor

    return rows


def row_distance_sum(rows: list[int]) -> int:
    distance_sum = row_sum = 0
    for row_index, row in enumerate(rows):
        distance_sum += row_index * row - row_sum
        row_sum += row
    return distance_sum


def solve_part_one(universe: list[str]) -> int:
    return solve_part_two(universe, 2)


def solve_part_two(universe: list[str], expansion_factor: int) -> int:
    row_sum = row_distance_sum(find_rows(universe, expansion_factor))
    transpose = ["".join(column) for column in zip(*universe)]
    column_sum = row_distance_sum(find_rows(transpose, expansion_factor))
    return row_sum + column_sum


def test():
    universe = read_and_parse("example.txt")
    part_one_answer = solve_part_one(universe)
    assert part_one_answer == 374
    part_two_answer = solve_part_two(universe, 10)
    assert part_two_answer == 1_030
    part_two_answer = solve_part_two(universe, 100)
    assert part_two_answer == 8_410


def main():
    universe = read_and_parse("input.txt")
    part_one_answer = solve_part_one(universe)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(universe, 1_000_000)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
