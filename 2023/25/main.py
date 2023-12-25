#!/usr/bin/env python3
import networkx as nx


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        g = nx.Graph()
        for line in file.read().splitlines():
            src, dsts = line.split(': ')
            for dst in dsts.split():
                g.add_edge(src, dst, capacity=1)
        return g


def solve_part_one(g) -> int:
    src, *dsts = list(g.nodes())
    for dst in dsts:
        cut_value, partition = nx.minimum_cut(g, src, dst)
        if cut_value == 3:
            side1, side2 = partition
            return len(side1) * len(side2)
    assert False


def test():
    a = read_and_parse("example.txt")
    part_one_answer = solve_part_one(a)
    assert part_one_answer == 54


def main():
    a = read_and_parse("input.txt")
    part_one_answer = solve_part_one(a)
    print(f"Part One: {part_one_answer}")


if __name__ == "__main__":
    test()
    main()
