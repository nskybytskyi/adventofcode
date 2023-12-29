#!/usr/bin/env python3
"""Clumsy Crucible"""
import collections
import functools
import heapq
from typing import Iterable


@functools.total_ordering
class Node(collections.namedtuple("Node", ["location", "direction", "count"])):
    """fancy named tuple"""

    def key(self) -> tuple[int, int, int, int, int]:
        return (
            self.location.real,
            self.location.imag,
            self.direction.real,
            self.direction.imag,
            self.count,
        )

    def __lt__(self, other) -> bool:
        return self.key() < other.key()

    def __eq__(self, other) -> bool:
        return self.key() == other.key()

    def __hash__(self) -> int:
        return hash(self.key())


class Grid:
    """2d heatloss_grid with complex indexing"""

    def __init__(self, raw: list[str]):
        self.lower_bound = self.upper_bound = 0
        self.raw = [list(map(int, line)) for line in raw]

    def shape(self) -> tuple[int, int]:
        return len(self.raw), len(self.raw[0])

    def set_bounds(self, lower_bound: int, upper_bound: int):
        self.lower_bound, self.upper_bound = lower_bound, upper_bound

    def __contains__(self, cell: complex) -> bool:
        row, col = int(cell.real), int(cell.imag)
        return 0 <= row < len(self.raw) and 0 <= col < len(self.raw[0])

    def __getitem__(self, cell: complex) -> int:
        return self.raw[int(cell.real)][int(cell.imag)]

    def get_neighbors(self, node: Node) -> Iterable[tuple[Node, int]]:
        if self.lower_bound <= node.count:
            for new_direction in 1j * node.direction, -1j * node.direction:
                new_node = Node(node.location + new_direction, new_direction, 1)
                if new_node.location in self:
                    yield new_node, self[new_node.location]

        if node.count < self.upper_bound:
            node = Node(node.location + node.direction, node.direction, node.count + 1)
            if node.location in self:
                yield node, self[node.location]


def read_and_parse(filename: str) -> Grid:
    with open(filename, "r", encoding="utf-8") as file:
        return Grid(file.read().splitlines())


def dijkstra(heatloss_grid: Grid, sources: list[Node]):
    distance = collections.defaultdict(lambda: 10**9)
    heap = []

    for source in sources:
        distance[source] = 0
        heapq.heappush(heap, (0, source))

    while heap:
        node_distance, node = heapq.heappop(heap)
        if node_distance != distance[node]:
            continue

        for next_node, edge_length in heatloss_grid.get_neighbors(node):
            if distance[next_node] > distance[node] + edge_length:
                distance[next_node] = distance[node] + edge_length
                heapq.heappush(heap, (distance[next_node], next_node))

    return distance


def solve_part_one(heatloss_grid: Grid) -> int:
    heatloss_grid.set_bounds(0, 3)
    distance = dijkstra(heatloss_grid, [Node(0, 1j, 0), Node(0, 1, 0)])
    rows, cols = heatloss_grid.shape()
    return min(
        node_distance
        for node, node_distance in distance.items()
        if node.location == rows - 1 + (cols - 1) * 1j
    )


def solve_part_two(heatloss_grid: Grid) -> int:
    heatloss_grid.set_bounds(4, 10)
    distance = dijkstra(heatloss_grid, [Node(0, 1j, 0), Node(0, 1, 0)])
    rows, cols = heatloss_grid.shape()
    return min(
        node_distance
        for node, node_distance in distance.items()
        if node.location == rows - 1 + (cols - 1) * 1j and node.count >= 4
    )


def test():
    heatloss_grid = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(heatloss_grid)
    assert part_one_answer == 102
    part_two_answer = solve_part_two(heatloss_grid)
    assert part_two_answer == 94

    heatloss_grid = read_and_parse("example-2.txt")
    part_two_answer = solve_part_two(heatloss_grid)
    assert part_two_answer == 71


def main():
    heatloss_grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(heatloss_grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(heatloss_grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
