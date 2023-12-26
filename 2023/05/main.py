#!/usr/bin/env python3
"""If You Give A Seed A Fertilizer"""
import collections
import itertools
from typing import Iterable, Optional


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


ValueRange = collections.namedtuple("ValueRange", ["start", "length"])


class MappingRange:
    """a linear mapping on a range"""

    def __init__(self, destination: int, source: int, length: int):
        self.destination, self.length = destination, length
        self.source_start = source
        self.source_end = source + length

    def apply_to_point(self, value: int) -> Optional[int]:
        if self.source_start <= value < self.source_end:
            return self.destination + value - self.source_start
        return None

    def apply_to_range(
        self, value_range: ValueRange
    ) -> Optional[tuple[ValueRange, ValueRange]]:
        """returns consumed range and its image if any"""
        start = max(self.source_start, value_range.start)
        end = min(self.source_end, value_range.start + value_range.length)

        if (length := end - start) > 0:
            consumed_range = ValueRange(start, length)
            offset = start - self.source_start
            image = ValueRange(self.destination + offset, length)
            return consumed_range, image

        return None


class PiecewiseLinearMapping:
    """a piecewise-linear mapping"""

    def __init__(self, ranges: Iterable[MappingRange]):
        self.ranges = list(ranges)

    def apply_to_point(self, value: int) -> int:
        for mapping_range in self.ranges:
            if (maybe := mapping_range.apply_to_point(value)) is not None:
                return maybe
        return value

    def apply_to_range(self, values: ValueRange) -> Iterable[ValueRange]:
        consumed_ranges = []
        for mapping_range in self.ranges:
            if (maybe := mapping_range.apply_to_range(values)) is not None:
                consumed_range, image = maybe
                consumed_ranges.append(consumed_range)
                yield image

        start = values.start
        for consumed_start, consumed_length in sorted(consumed_ranges):
            if start < consumed_start:
                yield ValueRange(start, consumed_start - start)
            start = consumed_start + consumed_length

        if start < (values_end := values.start + values.length):
            yield ValueRange(start, values_end - start)


def parse_mapping(map_raw: str) -> PiecewiseLinearMapping:
    return PiecewiseLinearMapping(
        MappingRange(*map(int, range_raw.split()))
        for range_raw in map_raw.split("\n")[1:]
    )


def read_and_parse(filename: str) -> tuple[list[int], list[PiecewiseLinearMapping]]:
    with open(filename, "r", encoding="utf-8") as file:
        raw_seeds, *raw_mappings = file.read().split("\n\n")
        seeds = list(map(int, raw_seeds.split(":")[1].split()))
        mappings = list(map(parse_mapping, raw_mappings))
        return seeds, mappings


def solve_part_one(values: list[int], mappings: list[PiecewiseLinearMapping]) -> int:
    for mapping in mappings:
        values = list(map(mapping.apply_to_point, values))
    return min(values)


def solve_part_two(seeds: list[int], mappings: list[PiecewiseLinearMapping]) -> int:
    ranges = list(itertools.starmap(ValueRange, batched(seeds, 2)))
    for mapping in mappings:
        ranges = list(
            itertools.chain.from_iterable(map(mapping.apply_to_range, ranges))
        )
    return min(range_.start for range_ in ranges)


def test():
    values, maps_raw = read_and_parse("example.txt")
    part_one_answer = solve_part_one(values, maps_raw)
    assert part_one_answer == 35
    part_two_answer = solve_part_two(values, maps_raw)
    assert part_two_answer == 46


def main():
    seeds, maps_raw = read_and_parse("input.txt")
    part_one_answer = solve_part_one(seeds, maps_raw)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(seeds, maps_raw)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
