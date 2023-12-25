#!/usr/bin/env python3
"""Haunted Wasteland"""
import itertools
import math
import typing as tp

Graph = tp.Mapping[str, tuple[int, int]]


def read_and_parse(filename: str) -> tuple[str, Graph]:
    with open(filename, "r", encoding="utf-8") as file:
        instructions, _, *graph_lines = file.read().splitlines()
        graph = {line[:3]: (line[7:10], line[12:15]) for line in graph_lines}
        return instructions, graph


def distance(
    graph: Graph,
    instructions: str,
    node: str,
    is_end: tp.Callable[[str], bool],
) -> int:
    for step, instruction in enumerate(itertools.cycle(instructions), start=1):
        node = graph[node][instruction == "R"]
        if is_end(node):
            return step
    assert False


def solve_part_one(data: tuple[str, Graph]) -> int:
    instructions, graph = data
    return distance(graph, instructions, "AAA", lambda node: node == "ZZZ")


def solve_part_two(data: tuple[str, Graph]) -> int:
    instructions, graph = data
    distances = (
        distance(graph, instructions, node, lambda node: node.endswith("Z"))
        for node in graph
        if node.endswith("A")
    )
    return math.lcm(*distances)


def test():
    data = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(data)
    assert part_one_answer == 2

    data = read_and_parse("example-2.txt")
    part_one_answer = solve_part_two(data)
    assert part_one_answer == 6

    data = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(data)
    assert part_two_answer == 6


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
