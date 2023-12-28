#!/usr/bin/env python3
"""Hot Springs"""
import collections
import functools
import itertools


Record = collections.namedtuple("Record", ["damaged", "groups"])


def parse_record(text: str) -> Record:
    records, raw_nums = text.split()
    nums = list(map(int, raw_nums.split(",")))
    return Record(records, nums)


def read_and_parse(filename: str) -> list[Record]:
    """condition records of which hot springs are damaged"""
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(parse_record, file.read().splitlines()))


def match(restored: tuple[str, ...], groups: list[int]) -> bool:
    """does s fit the description of nums"""
    return groups == [
        sum(1 for _ in grouper)
        for key, grouper in itertools.groupby(restored)
        if key == "#"
    ]


def brute_force(record: Record) -> int:
    """try all combinations of states"""
    gen = ("#." if letter == "?" else letter for letter in record.damaged)
    return sum(match(candidate, record.groups) for candidate in itertools.product(*gen))


def dynamic_programming(record: Record) -> int:
    """count continuations from a given state"""

    @functools.cache
    def num_ways(
        spring_index: int, group_index: int, current_group: int, last: str
    ) -> int:
        if spring_index == len(record.damaged):
            return group_index == len(record.groups)

        total = 0

        if record.damaged[spring_index] != "#" and not current_group:
            total += num_ways(spring_index + 1, group_index, 0, ".")

        if (
            record.damaged[spring_index] != "."
            and (current_group or last != "#")
            and group_index < len(record.groups)
        ):
            if current_group + 1 == record.groups[group_index]:
                total += num_ways(spring_index + 1, group_index + 1, 0, "#")
            else:
                total += num_ways(spring_index + 1, group_index, current_group + 1, "#")

        return total

    return num_ways(0, 0, 0, ".")


def solve_part_one(records: list[Record]) -> int:
    """count arrangements that fit the description"""
    return sum(map(brute_force, records))


def unfold_record(record: Record) -> Record:
    return Record("?".join(5 * [record.damaged]), 5 * record.groups)


def solve_part_two(records: list[Record]) -> int:
    """unfolded records"""
    unfolded_records = map(unfold_record, records)
    return sum(map(dynamic_programming, unfolded_records))


def test():
    springs = read_and_parse("example.txt")
    part_one_answer = solve_part_one(springs)
    assert part_one_answer == 21
    part_two_answer = solve_part_two(springs)
    assert part_two_answer == 525_152


def main():
    springs = read_and_parse("input.txt")
    part_one_answer = solve_part_one(springs)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(springs)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
