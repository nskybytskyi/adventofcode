#!/usr/bin/env python3
"""Haunted Wasteland"""
import itertools
import math
from typing import Callable


Graph = dict[str, tuple[str, str]]


def parse_edge(text: str) -> tuple[str, tuple[str, str]]:
    return text[:3], (text[7:10], text[12:15])


def read_and_parse(filename: str) -> tuple[str, Graph]:
    with open(filename, "r", encoding="utf-8") as file:
        instructions, raw_graph = file.read().split("\n\n")
        return instructions, dict(map(parse_edge, raw_graph.split("\n")))


def calculate_period(
    graph: Graph,
    instructions: str,
    node: str,
    is_end: Callable[[str], bool],
) -> int:
    for step, instruction in enumerate(itertools.cycle(instructions), start=1):
        if is_end(node := graph[node][instruction == "R"]):
            return step
    assert False


def solve_part_one(instructions: str, graph: Graph) -> int:
    return calculate_period(graph, instructions, "AAA", lambda node: node == "ZZZ")


def solve_part_two(instructions: str, graph: Graph) -> int:
    gen = (
        calculate_period(graph, instructions, node, lambda node: node.endswith("Z"))
        for node in graph
        if node.endswith("A")
    )
    return math.lcm(*gen)


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
