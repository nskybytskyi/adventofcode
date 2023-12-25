#!/usr/bin/env python3
"""A Long Walk"""
import sys
import collections
sys.setrecursionlimit(100_000)


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def solve_part_one(hiking_trails) -> int:
    rows, cols = len(hiking_trails), len(hiking_trails[0])
    seen = {(int(0), int(1))}

    def nei(row: int, col: int):
        mapping = {'.': [(row - 1, col), (row, col - 1),
                         (row, col + 1), (row + 1, col)],
                   '^': [(row - 1, col)], '<': [(row, col - 1)],
                   '>': [(row, col + 1)], 'v': [(row + 1, col)]}
        return mapping[hiking_trails[row][col]]

    longest_path = 0

    def backtrack(row: int, col: int):
        nonlocal longest_path
        if row == rows - 1 and col == cols - 2:
            longest_path = max(longest_path, len(seen))

        for next_row, next_col in nei(row, col):
            if (
                0 <= next_row < rows and
                0 <= next_col < cols and
                hiking_trails[next_row][next_col] != '#' and
                (next_row, next_col) not in seen
            ):
                seen.add((next_row, next_col))
                backtrack(next_row, next_col)
                seen.remove((next_row, next_col))

    backtrack(0, 1)
    return longest_path - 1


def get_neighbors(hiking_trails, row: int, col: int):
    nei = [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]
    for next_row, next_col in nei:
        if (
            0 <= next_row < len(hiking_trails) and
            0 <= next_col < len(hiking_trails[0]) and
            hiking_trails[next_row][next_col] != '#'
        ):
            yield next_row, next_col


def build_graph(hiking_trails: list[str]):
    rows, cols = len(hiking_trails), len(hiking_trails[0])
    graph = collections.defaultdict(list)

    for row in range(rows):
        for col in range(cols):
            if hiking_trails[row][col] == '#':
                continue
            for next_row, next_col in get_neighbors(hiking_trails, row, col):
                graph[row, col].append((next_row, next_col))

    return graph


def condense_graph(special, hiking_trails):
    condensed_graph = collections.defaultdict(list)
    for special_row, special_col in special:
        distance = {(special_row, special_col): 0}
        queue = collections.deque([(special_row, special_col)])
        while queue:
            row, col = queue.popleft()
            for next_row, next_col in get_neighbors(hiking_trails, row, col):
                if (next_row, next_col) in distance:
                    continue
                if (next_row, next_col) in special:
                    condensed_graph[special_row, special_col].append(
                        ((next_row, next_col), distance[row, col] + 1))
                else:
                    distance[next_row, next_col] = distance[row, col] + 1
                    queue.append((next_row, next_col))
    return condensed_graph


def solve_part_two(hiking_trails) -> int:
    rows, cols = len(hiking_trails), len(hiking_trails[0])

    graph = build_graph(hiking_trails)
    special = {(0, 1), (rows - 1, cols - 2)}
    for row in range(rows):
        for col in range(cols):
            if len(graph[row, col]) > 2:
                special.add((row, col))
    condensed_graph = condense_graph(special, hiking_trails)

    longest_path = 0
    seen = {(0, 1)}
    length = 0

    def backtrack(node):
        nonlocal longest_path, length
        if node == (rows - 1, cols - 2):
            longest_path = max(longest_path, length)

        for next_node, edge in condensed_graph[node]:
            if next_node in seen:
                continue
            length += edge
            seen.add(next_node)
            backtrack(next_node)
            seen.remove(next_node)
            length -= edge

    backtrack((0, 1))
    return longest_path


def test():
    hiking_trails = read_and_parse("example.txt")
    part_one_answer = solve_part_one(hiking_trails)
    assert part_one_answer == 94
    part_two_answer = solve_part_two(hiking_trails)
    assert part_two_answer == 154


def main():
    hiking_trails = read_and_parse("input.txt")
    part_one_answer = solve_part_one(hiking_trails)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(hiking_trails)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
