#!/usr/bin/env python3
"""Camel cards"""
import collections


def read_and_parse(filename: str) -> list[tuple[str, int]]:
    games = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            hand, bid = line.split()
            games.append((hand, int(bid)))
    return games


def part1_key(hand: str) -> list[int]:
    hand_type = sorted(collections.Counter(hand).values(), reverse=True)
    hand_value = [-"AKQJT98765432".index(card) for card in hand]
    return hand_type + hand_value


def part2_key(hand: str) -> list[int]:
    counter = collections.Counter(hand)
    jokers = counter["J"]
    del counter["J"]

    hand_value = [-"AKQT98765432J".index(card) for card in hand]
    hand_type = sorted(counter.values(), reverse=True) or [0]
    hand_type[0] += jokers

    return hand_type + hand_value


def score(ordered_games: list[tuple[str, int]]) -> int:
    return sum(rank * bid for rank, (_, bid) in enumerate(ordered_games, start=1))


def solve_part_one(camel_cards: list[tuple[str, int]]) -> int:
    camel_cards.sort(key=lambda pair: part1_key(pair[0]))
    return score(camel_cards)


def solve_part_two(camel_cards: list[tuple[str, int]]) -> int:
    camel_cards.sort(key=lambda pair: part2_key(pair[0]))
    return score(camel_cards)


def test():
    camel_cards = read_and_parse("example.txt")
    part_one_answer = solve_part_one(camel_cards)
    assert part_one_answer == 6_440
    part_two_answer = solve_part_two(camel_cards)
    assert part_two_answer == 5_905


def main():
    camel_cards = read_and_parse("input.txt")
    part_one_answer = solve_part_one(camel_cards)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(camel_cards)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
