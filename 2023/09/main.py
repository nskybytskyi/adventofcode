#!/usr/bin/env python3
"""Mirage Maintenance"""
import itertools


def read_and_parse(filename: str) -> list[list[int]]:
    with open(filename, "r", encoding="utf-8") as file:
        return [list(map(int, line.split())) for line in file.read().splitlines()]


def predict(nums: list[int]) -> int:
    diff = [curr - prev for prev, curr in itertools.pairwise(nums)]
    return nums[-1] + (predict(diff) if any(diff) else 0)


def solve_part_one(data: list[list[int]]) -> int:
    return sum(predict(row) for row in data)


def solve_part_two(data: list[list[int]]) -> int:
    return sum(predict(row[::-1]) for row in data)


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 114
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 2


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
