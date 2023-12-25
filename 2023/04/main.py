#!/usr/bin/env python3
"""Scratchcards"""


def read_and_parse(filename: str) -> list[tuple[list[int], list[int]]]:
    cards = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            _, nums = line.split(": ")
            win, my = nums.split(" | ")
            win_nums = list(map(int, win.split()))
            my_nums = list(map(int, my.split()))
            cards.append((win_nums, my_nums))
    return cards


def solve_part_one(data: list[tuple[list[int], list[int]]]) -> int:
    score = 0
    for win, my in data:
        if matches := len(set(win) & set(my)):
            score += 1 << (matches - 1)
    return score


def solve_part_two(data: list[tuple[list[int], list[int]]]) -> int:
    copies = [1] * len(data)
    for i, (win, my) in enumerate(data):
        matches = len(set(win) & set(my))
        for j in range(i + 1, i + matches + 1):
            copies[j] += copies[i]
    return sum(copies)


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 13
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 30


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
