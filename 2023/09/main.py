#!/usr/bin/env python3
"""Mirage Maintenance"""
import itertools


def parse_nums(text: str) -> list[int]:
    return list(map(int, text.split()))


def read_and_parse(filename: str) -> list[list[int]]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(parse_nums, file.read().splitlines()))


def predict(nums: list[int]) -> int:
    diff = [curr - prev for prev, curr in itertools.pairwise(nums)]
    return nums[-1] + (predict(diff) if any(diff) else 0)


def solve_part_one(records: list[list[int]]) -> int:
    return sum(map(predict, records))


def solve_part_two(records: list[list[int]]) -> int:
    return sum(predict(record[::-1]) for record in records)


def test():
    records = read_and_parse("example.txt")
    part_one_answer = solve_part_one(records)
    assert part_one_answer == 114
    part_two_answer = solve_part_two(records)
    assert part_two_answer == 2


def main():
    records = read_and_parse("input.txt")
    part_one_answer = solve_part_one(records)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(records)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
