#!/usr/bin/env python3
"""The contraption Will Be Lava"""
import collections


def breadth_first_search(
    contraption: list[str], initial_location: complex, initial_direction: complex
) -> int:
    seen = set()
    queue = collections.deque([(initial_location, initial_direction)])

    while queue:
        location, direction = queue.popleft()

        if (
            location.real < 0
            or location.real >= len(contraption)
            or location.imag < 0
            or location.imag >= len(contraption[0])
            or (location, direction) in seen
        ):
            continue

        seen.add((location, direction))
        cell = contraption[int(location.real)][int(location.imag)]

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


def solve_part_one(contraption: list[str]) -> int:
    return breadth_first_search(contraption, 0, 1j)


def solve_part_two(contraption: list[str]) -> int:
    rows, cols = len(contraption), len(contraption[0])

    ans = 0
    for row in range(rows):
        val = breadth_first_search(contraption, row, 1j)
        ans = max(ans, val)
        val = breadth_first_search(contraption, row + (cols - 1) * 1j, -1j)
        ans = max(ans, val)
    for col in range(cols):
        val = breadth_first_search(contraption, col * 1j, 1)
        ans = max(ans, val)
        val = breadth_first_search(contraption, rows - 1 + col * 1j, -1)
        ans = max(ans, val)
    return ans


def test():
    contraption = read_and_parse("example.txt")
    part_one_answer = solve_part_one(contraption)
    assert part_one_answer == 46
    part_two_answer = solve_part_two(contraption)
    assert part_two_answer == 51


def main():
    contraption = read_and_parse("input.txt")
    part_one_answer = solve_part_one(contraption)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(contraption)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
