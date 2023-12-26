#!/usr/bin/env python3
"""Scratchcards"""
import collections


Scratchcard = collections.namedtuple(
    "Scratchcard", ["winning_numbers", "numbers_you_have"]
)


def parse_numbers(text: str) -> set[int]:
    return set(map(int, text.split()))


def parse_scratchcard(text: str) -> Scratchcard:
    return Scratchcard(*map(parse_numbers, text.split(": ")[1].split(" | ")))


def read_and_parse(filename: str) -> list[Scratchcard]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(parse_scratchcard, file.read().splitlines()))


def count_matches(scratchcard: Scratchcard) -> int:
    return len(scratchcard.winning_numbers & scratchcard.numbers_you_have)


def solve_part_one(scratchcards: list[Scratchcard]) -> int:
    return sum(
        1 << (matches - 1)
        for scratchcard in scratchcards
        if (matches := count_matches(scratchcard))
    )


def solve_part_two(scratchcards: list[Scratchcard]) -> int:
    copies = [1] * len(scratchcards)
    for i, scratchcard in enumerate(scratchcards):
        for j in range(count_matches(scratchcard)):
            copies[i + 1 + j] += copies[i]
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
