#!/usr/bin/env python3
"""Camel cards"""
import collections


Game = collections.namedtuple("Game", ["hand", "bid"])


def parse_game(text: str) -> Game:
    hand, bid = text.split()
    return Game(hand, int(bid))


def read_and_parse(filename: str) -> list[Game]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(parse_game, file.read().splitlines()))


def default_key(hand: str) -> list[int]:
    hand_type = sorted(collections.Counter(hand).values(), reverse=True)
    hand_value = [-"AKQJT98765432".index(card) for card in hand]
    return hand_type + hand_value


def jokers_key(hand: str) -> list[int]:
    counter = collections.Counter(hand)
    jokers = counter["J"]
    del counter["J"]

    hand_value = [-"AKQT98765432J".index(card) for card in hand]
    hand_type = sorted(counter.values(), reverse=True) or [0]
    hand_type[0] += jokers

    return hand_type + hand_value


def score(games: list[Game]) -> int:
    return sum(rank * bid for rank, (_, bid) in enumerate(games, start=1))


def solve_part_one(games: list[Game]) -> int:
    return score(sorted(games, key=lambda game: default_key(game.hand)))


def solve_part_two(games: list[Game]) -> int:
    return score(sorted(games, key=lambda game: jokers_key(game.hand)))


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
