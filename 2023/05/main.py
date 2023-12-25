#!/usr/bin/env python3
"""If You Give A Seed A Fertilizer"""
import collections
import itertools
import typing as tp


ValueRange = collections.namedtuple("ValueRange", ["start", "length"])


class MappingRange:
    """a linear mapping on a range"""
    def __init__(self, destination: int, source: int, length: int):
        self.destination, self.length = destination, length
        self.source_start = source
        self.source_end = source + length

    def apply_to_point(self, value: int) -> tp.Optional[int]:
        if value < self.source_start or self.source_end <= value:
            return None
        offset = value - self.source_start
        return self.destination + offset

    def apply_to_range(
        self, value_range: ValueRange
    ) -> tp.Optional[tuple[ValueRange, ValueRange]]:
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
    def __init__(self, ranges: list[MappingRange]):
        self.ranges = ranges

    def apply_to_point(self, value: int) -> int:
        for mapping_range in self.ranges:
            if (maybe := mapping_range.apply_to_point(value)) is not None:
                return maybe
        return value

    def apply_to_range(self, values: ValueRange) -> tp.Iterable[ValueRange]:
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


def read_and_parse(filename: str) -> tuple[list[int], list[list[MappingRange]]]:
    def parse_mapping_ranges(map_raw: str) -> list[MappingRange]:
        return [MappingRange(*map(int, range_raw.split())) for range_raw in map_raw.split('\n')[1:]]

    with open(filename, "r", encoding="utf-8") as file:
        seeds_raw, *maps_raw = file.read().split('\n\n')
        seeds = list(map(int, seeds_raw.split(":")[1].split()))
        maps = list(map(parse_mapping_ranges, maps_raw))
        return seeds, maps


def solve_part_one(data: tuple[list[int], list[list[MappingRange]]]) -> int:
    values, maps_raw = data
    for map_raw in maps_raw:
        map_ = PiecewiseLinearMapping(map_raw)
        values = [map_.apply_to_point(value) for value in values]
    return min(values)


def solve_part_two(data: tuple[list[int], list[list[MappingRange]]]) -> int:
    seeds, maps_raw = data
    ranges = [
        ValueRange(seeds[2 * i], seeds[2 * i + 1]) for i in range(len(seeds) >> 1)
    ]

    for map_raw in maps_raw:
        map_ = PiecewiseLinearMapping(map_raw)
        ranges = list(
            itertools.chain.from_iterable(
                map_.apply_to_range(range_) for range_ in ranges
            )
        )

    return min(range_.start for range_ in ranges)


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 35
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 46


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
