#!/usr/bin/env python3
"""Wait For It"""
import bisect
import math


def parse_nums(text: str) -> list[int]:
    return list(map(int, text.split()))


def read_and_parse(filename: str) -> tuple[list[int], ...]:
    with open(filename, "r", encoding="utf-8") as file:
        lines = (line.split(":")[1] for line in file.read().splitlines())
        return tuple(map(parse_nums, lines))


def solve_part_one(times: list[int], dists: list[int]) -> int:
    return math.prod(
        sum((time - hold) * hold > dist for hold in range(1, time))
        for time, dist in zip(times, dists)
    )


def fix_kerning(nums: list[int]) -> int:
    return int("".join(map(str, nums)))


def solve_part_two(times: list[int], dists: list[int]) -> int:
    time, dist = map(fix_kerning, (times, dists))
    upper_bound = bisect.bisect_right(
        range(time // 2 + 1),
        dist,
        key=lambda hold: (time - hold) * hold,
    )
    return time - 2 * upper_bound + 1


def test():
    times, dists = read_and_parse("example.txt")
    part_one_answer = solve_part_one(times, dists)
    assert part_one_answer == 288
    part_two_answer = solve_part_two(times, dists)
    assert part_two_answer == 71_503


def main():
    times, dists = read_and_parse("input.txt")
    part_one_answer = solve_part_one(times, dists)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(times, dists)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
