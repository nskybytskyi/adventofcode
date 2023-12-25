#!/usr/bin/env python3
"""Snowverload"""
import networkx as nx


def read_and_parse(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        graph = nx.Graph()
        for line in file.read().splitlines():
            src, dsts = line.split(': ')
            for dst in dsts.split():
                graph.add_edge(src, dst, capacity=1)
        return graph


def solve_part_one(graph) -> int:
    src, *dsts = list(graph.nodes())
    for dst in dsts:
        cut_value, partition = nx.minimum_cut(graph, src, dst)
        if cut_value == 3:
            side1, side2 = partition
            return len(side1) * len(side2)
    assert False


def test():
    graph = read_and_parse("example.txt")
    part_one_answer = solve_part_one(graph)
    assert part_one_answer == 54


def main():
    graph = read_and_parse("input.txt")
    part_one_answer = solve_part_one(graph)
    print(f"Part One: {part_one_answer}")


if __name__ == "__main__":
    test()
    main()
