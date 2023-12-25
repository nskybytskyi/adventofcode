#!/usr/bin/env python3
"""Clumsy Crucible"""
import collections
import heapq
import math


def read_and_parse(filename: str) -> list[list[int]]:
    with open(filename, "r", encoding="utf-8") as file:
        return [list(map(int, line)) for line in file.read().splitlines()]


def dijkstra(sources, get_neighbors):
    distance = collections.defaultdict(lambda: math.inf)
    heap = []

    for source in sources:
        distance[source] = 0
        heapq.heappush(heap, (0, source))

    while heap:
        node_distance, node = heapq.heappop(heap)
        if node_distance != distance[node]:
            continue

        for next_node, edge_length in get_neighbors(node):
            if distance[next_node] > distance[node] + edge_length:
                distance[next_node] = distance[node] + edge_length
                heapq.heappush(heap, (distance[next_node], next_node))

    return distance


def solve_part_one(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def get_neighbors(node):
        row, col, dir_row, dir_col, cnt = node

        if cnt < 3:
            next_row, next_col = row + dir_row, col + dir_col
            next_node = next_row, next_col, dir_row, dir_col, cnt + 1
            if 0 <= next_row < rows and 0 <= next_col < cols:
                yield next_node, grid[next_row][next_col]

        for next_dir_row, next_dir_col in (dir_col, -dir_row), (-dir_col, dir_row):
            next_row, next_col = row + next_dir_row, col + next_dir_col
            next_node = next_row, next_col, next_dir_row, next_dir_col, 1
            if 0 <= next_row < rows and 0 <= next_col < cols:
                yield next_node, grid[next_row][next_col]

    distance = dijkstra(((0, 0, 0, 1, 0), (0, 0, 1, 0, 0)), get_neighbors)

    return min(
        node_distance
        for (row, col, *_), node_distance in distance.items()
        if row == rows - 1 and col == cols - 1
    )


def solve_part_two(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def get_neighbors(node):
        row, col, dir_row, dir_col, cnt = node

        if cnt < 10:
            next_row, next_col = row + dir_row, col + dir_col
            next_node = next_row, next_col, dir_row, dir_col, cnt + 1
            if 0 <= next_row < rows and 0 <= next_col < cols:
                yield next_node, grid[next_row][next_col]

        if cnt >= 4:
            for next_dir_row, next_dir_col in (dir_col, -dir_row), (-dir_col, dir_row):
                next_row, next_col = row + next_dir_row, col + next_dir_col
                next_node = next_row, next_col, next_dir_row, next_dir_col, 1
                if 0 <= next_row < rows and 0 <= next_col < cols:
                    yield next_node, grid[next_row][next_col]

    distance = dijkstra(((0, 0, 0, 1, 0), (0, 0, 1, 0, 0)), get_neighbors)

    return min(
        node_distance
        for (row, col, *_, cnt), node_distance in distance.items()
        if row == rows - 1 and col == cols - 1 and cnt >= 4
    )


def test():
    grid = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(grid)
    assert part_one_answer == 102
    part_two_answer = solve_part_two(grid)
    assert part_two_answer == 94

    grid = read_and_parse("example-2.txt")
    part_two_answer = solve_part_two(grid)
    assert part_two_answer == 71


def main():
    grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
