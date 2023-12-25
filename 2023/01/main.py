#!/usr/bin/env python3
"""Trebuchet?!"""
import string


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def recover_part_one(line: str) -> int:
    present = [digit for digit in string.digits if digit in line]
    first_value = min(present, key=lambda digit: line.index(str(digit)))
    last_value = max(present, key=lambda digit: line.rindex(str(digit)))
    return int(first_value + last_value)


def recover_part_two(line: str) -> int:
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def value(word: str) -> int:
        if word in words:
            return words.index(word) + 1
        return int(word)

    present = [digit for digit in list(string.digits) + words if digit in line]
    first_word = min(present, key=lambda digit: line.index(str(digit)))
    last_word = max(present, key=lambda digit: line.rindex(str(digit)))

    return 10 * value(first_word) + value(last_word)


def solve_part_one(lines: list[str]) -> int:
    return sum(map(recover_part_one, lines))


def solve_part_two(lines: list[str]) -> int:
    return sum(map(recover_part_two, lines))


def test():
    lines = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(lines)
    assert part_one_answer == 142

    lines = read_and_parse("example-2.txt")
    part_two_answer = solve_part_two(lines)
    assert part_two_answer == 281


def main():
    lines = read_and_parse("input.txt")
    part_one_answer = solve_part_one(lines)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(lines)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
