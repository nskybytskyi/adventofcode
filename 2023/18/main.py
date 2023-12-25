#!/usr/bin/env python3
"""Lavaduct Lagoon"""


def read_and_parse(filename: str) -> list[list[str]]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(list, file.read().splitlines()))


def solve_part_one(_) -> int:
    return 0


def solve_part_two(_) -> str:
    return 0


def test():
    pass


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
