#!/usr/bin/env python3
"""Haunted Wasteland"""
import itertools
import math
import typing as tp

Graph = tp.Mapping[str, tuple[str, str]]


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


def solve_part_one(instructions: str, graph: Graph) -> int:
    return distance(graph, instructions, "AAA", lambda node: node == "ZZZ")


def solve_part_two(instructions: str, graph: Graph) -> int:
    distances = (
        distance(graph, instructions, node, lambda node: node.endswith("Z"))
        for node in graph
        if node.endswith("A")
    )
    return math.lcm(*distances)


def test():
    instructions, graph = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(instructions, graph)
    assert part_one_answer == 2

    instructions, graph = read_and_parse("example-2.txt")
    part_one_answer = solve_part_two(instructions, graph)
    assert part_one_answer == 6

    instructions, graph = read_and_parse("example-3.txt")
    part_two_answer = solve_part_two(instructions, graph)
    assert part_two_answer == 6


def main():
    instructions, graph = read_and_parse("input.txt")
    part_one_answer = solve_part_one(instructions, graph)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(instructions, graph)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
