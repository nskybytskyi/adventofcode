#!/usr/bin/env python3
"""Pipe Maze"""
import collections


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def nei(grid, row, col):
    neighbors = [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]

    if grid[row][col] == "S":
        return [
            (nr, nc)
            for nr, nc in neighbors
            if (row, col) in nei(grid, nr, nc)
        ]

    mapping = {'|': [0, 3], '-': [1, 2], 'L': [0, 2], 'J': [0, 1], '7': [1, 3], 'F': [2, 3]}
    return [neighbors[idx] for idx in mapping[grid[row][col]]]


def find_s(grid):
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "S":
                return row, col
    assert False


def solve_part_one(pipe_grid: list[str]) -> int:
    rows, cols = len(pipe_grid), len(pipe_grid[0])
    start_row, start_col = find_s(pipe_grid)
    queue = collections.deque([(start_row, start_col)])
    dist = [[-1] * cols for _ in range(rows)]
    dist[start_row][start_col] = 0

    while queue:
        row, col = queue.popleft()
        for next_row, next_col in nei(pipe_grid, row, col):
            if 0 <= next_row < rows and 0 <= next_col < cols and dist[next_row][next_col] == -1:
                queue.append((next_row, next_col))
                dist[next_row][next_col] = dist[row][col] + 1

    return max(dist[row][col] for row in range(rows) for col in range(cols))


def area(fig: list[tuple[int, int]]) -> float:
    res = 0
    for i, curr in enumerate(fig):
        prev = fig[i - 1] if i else fig[-1]
        res += (prev[0] - curr[0]) * (prev[1] + curr[1])
    return abs(res / 2)


def solve_part_two(pipe_grid: list[str]) -> float:
    rows, cols = len(pipe_grid), len(pipe_grid[0])
    start_row, start_col = find_s(pipe_grid)
    path = [(start_row, start_col)]

    while len(path) == 1 or path[-1] != path[0]:
        row, col = path[-1]
        for next_row, next_col in nei(pipe_grid, row, col):
            if (
                0 <= next_row < rows
                and 0 <= next_col < cols
                and (len(path) < 2 or (next_row, next_col) != path[-2])
            ):
                path.append((next_row, next_col))
                break

    bound = len(path) - 1
    path = [(r, c) for r, c in path if pipe_grid[r][c] not in "-|"]
    return area(path) + 1 - bound / 2


def test():
    pipe_grid = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(pipe_grid)
    assert part_one_answer == 4
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 1

    pipe_grid = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 4

    pipe_grid = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 4

    pipe_grid = read_and_parse("example-4.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 4

    pipe_grid = read_and_parse("example-5.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 8

    pipe_grid = read_and_parse("example-6.txt")
    part_two_answer = solve_part_two(pipe_grid)
    assert part_two_answer == 10


def main():
    pipe_grid = read_and_parse("input.txt")
    part_one_answer = solve_part_one(pipe_grid)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(pipe_grid)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
