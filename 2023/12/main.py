#!/usr/bin/env python3
"""Hot Springs"""
import functools
import itertools


def read_and_parse(filename: str) -> list[tuple[str, list[int]]]:
    """condition records of which hot springs are damaged"""
    rows = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            records, raw_nums = line.split()
            nums = list(map(int, raw_nums.split(",")))
            rows.append((records, nums))
    return rows


def match(records: str, nums: list[int]) -> bool:
    """does s fit the description of nums"""
    return nums == [
        sum(1 for _ in grouper)
        for key, grouper in itertools.groupby(records)
        if key == "#"
    ]

def brute_force(records: str, nums: list[int]) -> int:
    """try all combinations of states"""
    gen = ("#." if letter == "?" else letter for letter in records)
    return sum(match(candidate, nums) for candidate in itertools.product(*gen))


def dynamic_programming(records: str, nums: list[int]) -> int:
    """count continuations from a given state"""

    @functools.cache
    def num_ways(i: int, j: int, curr: int, prev: str) -> int:
        if i == len(records):
            return j == len(nums)

        ans = 0

        if records[i] != "#" and not curr:
            ans += num_ways(i + 1, j, 0, ".")

        if records[i] != "." and (curr or prev != "#") and j < len(nums):
            if curr + 1 == nums[j]:
                ans += num_ways(i + 1, j + 1, 0, "#")
            else:
                ans += num_ways(i + 1, j, curr + 1, "#")

        return ans

    return num_ways(0, 0, 0, ".")


def solve_part_one(data: list[tuple[str, list[int]]]) -> int:
    """count arrangements that fit the description"""
    return sum(brute_force(s, nums) for s, nums in data)


def solve_part_two(data: list[tuple[str, list[int]]]) -> int:
    """unfolded records"""
    return sum(dynamic_programming("?".join(5 * [s]), 5 * nums) for s, nums in data)


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 21
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 525_152


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
