#!/usr/bin/env python3
"""Step Counter"""
import collections


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def solve_part_one(grid: list[str], steps: int = 64) -> int:
    rows, cols = len(grid), len(grid[0])
    start_row = start_col = -1
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'S':
                start_row, start_col = row, col
    queue = [{(start_row, start_col)}]
    for i in range(steps):
        queue.append(set())
        for row, col in queue[i]:
            nei = (row-1,col),(row,col-1),(row,col+1),(row+1,col)
            for next_row, next_col in nei:
                if (
                    0 <= next_row < rows and
                    0 <= next_col < cols and
                    grid[next_row][next_col] != '#'
                ):
                    queue[i + 1].add((next_row, next_col))
    return len(queue[steps])


def solve_part_two_naive(grid: list[str], steps: int) -> int:
    rows, cols = len(grid), len(grid[0])
    start_row = start_col = -1
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'S':
                start_row, start_col = row, col
    seen = {(start_row, start_col)}
    total = 0
    queue = collections.deque([(start_row, start_col)])
    for i in range(steps):
        if i % 2 == steps % 2:
            total += len(queue)
        for _ in range(len(queue)):
            row, col = queue.popleft()
            nei = (row-1,col),(row,col-1),(row,col+1),(row+1,col)
            for next_row, next_col in nei:
                if (
                    grid[next_row % rows][next_col % cols] != '#' and
                    (next_row, next_col) not in seen
                ):
                    seen.add((next_row, next_col))
                    queue.append((next_row, next_col))
    return total + len(queue)


def solve_part_two(grid: list[str], steps: int = 26_501_365) -> int:
    size = len(grid)
    midpoint = size >> 1

    def key(state):
        row, col, parity = state
        return row % size, col % size, parity, row >= midpoint, col >= midpoint

    start = midpoint, midpoint, 0
    queue = collections.deque([start])
    distance = {key(start): 0}
    unique = collections.defaultdict(set)
    unique[key(start)].add(start)

    while queue:
        old_state = queue.popleft()
        old_group = key(old_state)
        row, col, parity = old_state

        nei = (row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)
        for next_row, next_col in nei:
            if grid[next_row % size][next_col % size] == '#':
                continue

            new_state = next_row, next_col, 1 - parity
            new_group = key(new_state)

            if (
                new_group not in distance or (
                    distance[new_group] == distance[old_group] + 1 and
                    new_state not in unique[new_group]
                )
            ):
                queue.append(new_state)
                distance[new_group] = distance[old_group] + 1
                unique[new_group].add(new_state)

    total = 0

    for group, distance in distance.items():
        row, col, parity, *_ = group
        if parity != steps & 1 or steps < distance:
            continue

        blocks = (steps - distance) // (2 * size) + 1
        if len(unique[group]) == 1:
            total += blocks**2
        elif len(unique[group]) == 2:
            total += blocks * (blocks + 1)
        else:
            assert False

    return total


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data, 6)
    assert part_one_answer == 16

    part_one_answer = solve_part_two_naive(data, 6)
    assert part_one_answer == 16
    part_two_answer = solve_part_two_naive(data, 10)
    assert part_two_answer == 50
    part_two_answer = solve_part_two_naive(data, 50)
    assert part_two_answer == 1_594
    part_two_answer = solve_part_two_naive(data, 100)
    assert part_two_answer == 6_536
    part_two_answer = solve_part_two_naive(data, 500)
    assert part_two_answer == 167_004
    # part_two_answer = solve_part_two_naive(data, 1000)
    # assert part_two_answer == 668_697
    # part_two_answer = solve_part_two_naive(data, 5000)
    # assert part_two_answer == 16_733_044

    data = read_and_parse("input.txt")
    part_two_answer = solve_part_two(data, 10)
    assert part_two_answer == 103
    part_two_answer = solve_part_two(data, 50)
    assert part_two_answer == 2_272
    part_two_answer = solve_part_two(data, 100)
    assert part_two_answer == 9_102
    part_two_answer = solve_part_two(data, 500)
    assert part_two_answer == 223_017
    part_two_answer = solve_part_two(data, 1000)
    assert part_two_answer == 890_178


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
