#!/usr/bin/env python3
"""Lens Library"""
import collections
import functools
import re


def custom_hash(seq: str) -> int:
    return functools.reduce(lambda acc, val: 17 * (acc + ord(val)) % 256, seq, 0)


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()[0].split(",")


def solve_part_one(instructions: list[str]) -> int:
    return sum(custom_hash(instruction) for instruction in instructions)


def solve_part_two(instructions: list[str]) -> int:
    boxes = collections.defaultdict(dict)

    remove = re.compile("([a-z]+)-")
    assign = re.compile("([a-z]+)=([0-9])")

    for instruction in instructions:
        if (match_ := remove.match(instruction)) is not None:
            label = match_[1]
            box = boxes[custom_hash(label)]
            box.pop(label, None)
        elif (match_ := assign.match(instruction)) is not None:
            label, focal_length = match_.groups()
            box = boxes[custom_hash(label)]
            box[label] = int(focal_length)
        else:
            assert False

    power = 0
    for box_index, box in boxes.items():
        for lens_index, focal_length in enumerate(box.values()):
            power += (box_index + 1) * (lens_index + 1) * focal_length
    return power


def test():
    instructions = read_and_parse("example.txt")
    part_one_answer = solve_part_one(instructions)
    assert part_one_answer == 1320
    part_two_answer = solve_part_two(instructions)
    assert part_two_answer == 145


def main():
    instructions = read_and_parse("input.txt")
    part_one_answer = solve_part_one(instructions)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(instructions)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
