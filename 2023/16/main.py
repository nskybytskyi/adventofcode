#!/usr/bin/env python3
"""The Floor Will Be Lava"""
import collections


def breadth_first_search(
    grid: list[str], initial_location: complex, initial_direction: complex
) -> int:
    seen = set()
    queue = collections.deque([(initial_location, initial_direction)])

    while queue:
        location, direction = queue.popleft()

        if (
            location.real < 0
            or location.real >= len(grid)
            or location.imag < 0
            or location.imag >= len(grid[0])
            or (location, direction) in seen
        ):
            continue

        seen.add((location, direction))
        cell = grid[int(location.real)][int(location.imag)]

        if cell == "|" and direction.imag:
            queue.append((location + 1, 1))
            queue.append((location - 1, -1))
        elif cell == "-" and direction.real:
            queue.append((location + 1j, 1j))
            queue.append((location - 1j, -1j))
        elif cell == "\\":
            direction = direction.imag + direction.real * 1j
            queue.append((location + direction, direction))
        elif cell == "/":
            direction = direction.imag + direction.real * 1j
            queue.append((location - direction, -direction))
        else:
            queue.append((location + direction, direction))

    return len({location for location, _ in seen})


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def solve_part_one(grid: list[str]) -> int:
    return breadth_first_search(grid, 0, 1j)


def solve_part_two(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])

    ans = 0
    for row in range(rows):
        ans = max(ans, breadth_first_search(grid, row, 1j))
        ans = max(ans, breadth_first_search(grid, row + (cols - 1) * 1j, -1j))
    for col in range(cols):
        ans = max(ans, breadth_first_search(grid, col * 1j, 1))
        ans = max(ans, breadth_first_search(grid, rows - 1 + col * 1j, -1))
    return ans


def test():
    instructions = read_and_parse("example.txt")
    part_one_answer = solve_part_one(instructions)
    assert part_one_answer == 46
    part_two_answer = solve_part_two(instructions)
    assert part_two_answer == 51


def main():
    instructions = read_and_parse("input.txt")
    part_one_answer = solve_part_one(instructions)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(instructions)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
