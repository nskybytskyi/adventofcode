#!/usr/bin/env python3
"""Wait For It"""
import bisect
import math


def read_and_parse(filename: str) -> tuple[list[int], list[int]]:
    with open(filename, "r", encoding="utf-8") as file:
        raw_times, raw_dists = file.read().splitlines()
        times = list(map(int, raw_times.split(":")[1].split()))
        dists = list(map(int, raw_dists.split(":")[1].split()))
        return times, dists


def solve_part_one(data: tuple[list[int], list[int]]) -> int:
    gen = (
        sum((time - hold) * hold > dist for hold in range(1, time))
        for time, dist in zip(*data)
    )
    return math.prod(gen)


def solve_part_two(data: tuple[list[int], list[int]]) -> int:
    time, dist = (int("".join(map(str, row))) for row in data)
    lower_bound = bisect.bisect_left(
        range(time // 2 + 1),
        True,
        key=lambda hold: (time - hold) * hold > dist,
    )
    return time - 2 * lower_bound + 1


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 288
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 71_503


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
