#!/usr/bin/env python3
"""Cube Conundrum"""
import collections
import functools
import math
import operator


Draw = tuple[str, int]
Round = dict[str, int]
Game = list[Round]


def parse_draw(text: str) -> Draw:
    raw_balls, color = text.split()
    return color, int(raw_balls)


def parse_round(text: str) -> Round:
    return dict(map(parse_draw, text.split(", ")))


def parse_game(text: str) -> Game:
    return list(map(parse_round, text.split(": ")[1].split("; ")))


def read_and_parse(filename: str) -> list[Game]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(parse_game, file.read().splitlines()))


def compute_minimal_bag(game: Game) -> collections.Counter[str]:
    return functools.reduce(operator.or_, map(collections.Counter, game))


def solve_part_one(games: list[Game]) -> int:
    upper_bound = collections.Counter({"red": 12, "green": 13, "blue": 14})
    return sum(
        game_id
        for game_id, game in enumerate(games, start=1)
        if compute_minimal_bag(game) <= upper_bound
    )


def solve_part_two(games: list[Game]) -> int:
    return sum(math.prod(compute_minimal_bag(game).values()) for game in games)


def test():
    games = read_and_parse("example.txt")
    part_one_answer = solve_part_one(games)
    assert part_one_answer == 8
    part_two_answer = solve_part_two(games)
    assert part_two_answer == 2_286


def main():
    games = read_and_parse("input.txt")
    part_one_answer = solve_part_one(games)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(games)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
