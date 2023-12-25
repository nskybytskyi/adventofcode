#!/usr/bin/env python3
"""Pipe Maze"""
import collections


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def nei(grid, r, c):
    if grid[r][c] == "S":
        return [
            (nr, nc)
            for nr, nc in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            if (r, c) in nei(grid, nr, nc)
        ]
    elif grid[r][c] == "|":
        return (r - 1, c), (r + 1, c)
    elif grid[r][c] == "-":
        return (r, c - 1), (r, c + 1)
    elif grid[r][c] == "L":
        return (r - 1, c), (r, c + 1)
    elif grid[r][c] == "J":
        return (r - 1, c), (r, c - 1)
    elif grid[r][c] == "7":
        return (r, c - 1), (r + 1, c)
    elif grid[r][c] == "F":
        return (r, c + 1), (r + 1, c)
    else:
        return []


def find_s(grid):
    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "S":
                return row, col


def solve_part_one(data: list[str]) -> int:
    rows, cols = len(data), len(data[0])
    sr, sc = find_s(data)
    q = collections.deque([(sr, sc)])
    d = [[-1] * cols for _ in range(rows)]
    d[sr][sc] = 0

    while q:
        r, c = q.popleft()
        for nr, nc in nei(data, r, c):
            if 0 <= nr < rows and 0 <= nc < cols and d[nr][nc] == -1:
                q.append((nr, nc))
                d[nr][nc] = d[r][c] + 1

    return max(d[r][c] for r in range(rows) for c in range(cols))


def area(fig: list[tuple[int, int]]) -> float:
    res = 0
    for i in range(len(fig)):
        p = fig[i - 1] if i else fig[-1]
        q = fig[i]
        res += (p[0] - q[0]) * (p[1] + q[1])
    return abs(res / 2)


def solve_part_two(data: list[str]) -> int:
    rows, cols = len(data), len(data[0])
    sr, sc = find_s(data)
    path = [(sr, sc)]

    while len(path) == 1 or path[-1] != path[0]:
        r, c = path[-1]
        for nr, nc in nei(data, r, c):
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and (len(path) < 2 or (nr, nc) != path[-2])
            ):
                path.append((nr, nc))
                break

    bound = len(path) - 1
    path = [(r, c) for r, c in path if data[r][c] not in "-|"]
    return area(path) + 1 - bound / 2


def test():
    data = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 4
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 1

    data = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 4

    data = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 4

    data = read_and_parse("example-4.txt")
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 4

    data = read_and_parse("example-5.txt")
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 8

    data = read_and_parse("example-6.txt")
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 10


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
