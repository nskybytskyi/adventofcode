#!/usr/bin/env python3
"""Trebuchet?!"""


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def recover_calibration_value(
    text: str, words: list[str], values: dict[str, int]
) -> int:
    filtered_words = list(filter(text.__contains__, words))
    first_word = min(filtered_words, key=text.index)
    last_word = max(filtered_words, key=text.rindex)
    return 10 * values[first_word] + values[last_word]


def build_base_words_and_values() -> tuple[list[str], dict[str, int]]:
    return list("0123456789"), dict(zip("0123456789", range(10)))


def recover_part_one(text: str) -> int:
    digits, values = build_base_words_and_values()
    return recover_calibration_value(text, digits, values)


def recover_part_two(text: str) -> int:
    digits, values = build_base_words_and_values()
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    values.update(dict(zip(words, range(1, 10))))
    return recover_calibration_value(text, digits + words, values)


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
