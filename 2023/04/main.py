#!/usr/bin/env python3
"""Scratchcards"""


def read_and_parse(filename: str) -> list[tuple[list[int], list[int]]]:
    scratchcards = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            _, nums = line.split(": ")
            win_chunk, my_chunk = nums.split(" | ")
            win_nums = list(map(int, win_chunk.split()))
            my_nums = list(map(int, my_chunk.split()))
            scratchcards.append((win_nums, my_nums))
    return scratchcards


def solve_part_one(scratchcards: list[tuple[list[int], list[int]]]) -> int:
    score = 0
    for win_nums, my_nums in scratchcards:
        if matches := len(set(win_nums) & set(my_nums)):
            score += 1 << (matches - 1)
    return score


def solve_part_two(scratchcards: list[tuple[list[int], list[int]]]) -> int:
    copies = [1] * len(scratchcards)
    for i, (win_nums, my_nums) in enumerate(scratchcards):
        matches = len(set(win_nums) & set(my_nums))
        for j in range(i + 1, i + matches + 1):
            copies[j] += copies[i]
    return sum(copies)


def test():
    scratchcards = read_and_parse("example.txt")
    part_one_answer = solve_part_one(scratchcards)
    assert part_one_answer == 13
    part_two_answer = solve_part_two(scratchcards)
    assert part_two_answer == 30


def main():
    scratchcards = read_and_parse("input.txt")
    part_one_answer = solve_part_one(scratchcards)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(scratchcards)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
