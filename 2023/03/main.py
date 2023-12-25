#!/usr/bin/env python3
"""Gear Ratios"""
import collections
import typing as tp


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


Number = collections.namedtuple("Number", ["row", "start", "end", "value"])
Symbol = collections.namedtuple("Symbol", ["row", "column"])
Gear = collections.namedtuple("Gear", ["row", "column", "ratio"])


def numbers(nums_grid: list[str]) -> tp.Iterable[Number]:
    for row_index, row in enumerate(nums_grid):
        start = None

        for col_index, val in enumerate(row):
            if start is not None and not val.isdigit():
                if (value := row[start:col_index]) != "-":
                    yield Number(row_index, start, col_index, int(value))
                start = None

            if start is None and (val.isdigit() or val == "-"):
                start = col_index

        if start is not None and (value := row[start:]) != "-":
            yield Number(row_index, start, len(row), int(value))


def adjacent(nums_grid: list[str], number: Number) -> tp.Iterable[Symbol]:
    for row in (number.row - 1, number.row, number.row + 1):
        for col in range(number.start - 1, number.end + 1):
            if (
                0 <= row < len(nums_grid)
                and 0 <= col < len(nums_grid[row])
                and nums_grid[row][col] != "."
                and not nums_grid[row][col].isdigit()
            ):
                yield Symbol(row, col)


def part_numbers(nums_grid: list[str]) -> tp.Iterable[Number]:
    for number in numbers(nums_grid):
        if any(adjacent(nums_grid, number)):
            yield number


def symbols(nums_grid: list[str]) -> tp.Iterable[Symbol]:
    for row_index, row in enumerate(nums_grid):
        for col_index, val in enumerate(row):
            if val != "." and not val.isdigit():
                yield Symbol(row_index, col_index)


def gears(nums_grid: list[str]) -> tp.Iterable[Gear]:
    counter = collections.Counter()
    ratios = collections.defaultdict(list)

    for number in numbers(nums_grid):
        for symbol in adjacent(nums_grid, number):
            counter[symbol] += 1
            ratios[symbol].append(number.value)

    for symbol, count in counter.items():
        if count == 2:
            ratio = ratios[symbol][0] * ratios[symbol][1]
            yield Gear(symbol.row, symbol.column, ratio)


def solve_part_one(nums_grid: list[str]) -> int:
    return sum(abs(part_number.value) for part_number in part_numbers(nums_grid))


def solve_part_two(nums_grid: list[str]) -> int:
    return sum(gear.ratio for gear in gears(nums_grid))


def test():
    nums_grid = read_and_parse("example.txt")
    part_one_answer = solve_part_one(nums_grid)
    assert part_one_answer == 4361
    part_two_answer = solve_part_two(nums_grid)
    assert part_two_answer == 467_835


def main():
    nums_grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(nums_grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(nums_grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
