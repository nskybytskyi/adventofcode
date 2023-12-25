#!/usr/bin/env python3
"""Cube Conundrum"""
import collections
import functools
import math
import operator

Game = list[dict[str, int]]


def minimal_bag(game: Game) -> collections.Counter:
    counters = (collections.Counter(handful) for handful in game)
    return functools.reduce(operator.or_, counters)


def read_and_parse(filename: str) -> list[Game]:
    games = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            game = []
            _, raw_game = line.split(": ")
            for handful in raw_game.split("; "):
                draws = {}
                for draw in handful.split(", "):
                    balls, color = draw.split()
                    draws[color] = int(balls)
                game.append(draws)
            games.append(game)
    return games


def solve_part_one(data: list[Game]) -> int:
    limit = collections.Counter({"red": 12, "green": 13, "blue": 14})
    return sum(
        game_id
        for game_id, game in enumerate(data, start=1)
        if minimal_bag(game) <= limit
    )


def solve_part_two(data: list[Game]) -> int:
    return sum(math.prod(minimal_bag(game).values()) for game in data)


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 8
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 2_286


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
