#!/usr/bin/env python3
"""Pulse Propagation"""
import collections
import copy
import itertools
import math


def read_and_parse(filename: str) -> list[str]:
    graph = {}
    types = {"broadcaster": None}
    state = {}
    parents = collections.defaultdict(dict)

    with open(filename, "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            source, destinations = line.split(' -> ')

            if source != 'broadcaster':
                module_type = source[0]
                source = source[1:]
                types[source] = module_type

            state[source] = 0
            graph[source] = destinations.split(', ')

        for node, children in graph.items():
            for child in children:
                if child in types and types[child] == '&':
                    parents[child][node] = 0

        return graph, types, state, parents


def solve_part_one(graph, types, initial_state, initial_parents) -> int:
    state = copy.deepcopy(initial_state)
    parents = copy.deepcopy(initial_parents)
    count = {0: 0, 1: 0}

    for _ in range(1_000):
        queue = collections.deque([(None, "broadcaster", 0)])

        while queue:
            parent, module, pulse = queue.popleft()
            count[pulse] += 1
            if module not in types:
                continue

            if module == "broadcaster":
                for dest in graph[module]:
                    queue.append((module, dest, pulse))
            elif types[module] == '%':
                if pulse:
                    continue
                state[module] = not state[module]
                for dest in graph[module]:
                    queue.append((module, dest, state[module]))
            elif types[module] == '&':
                parents[module][parent] = pulse
                outgoing_pulse = not all(parents[module].values())
                for dest in graph[module]:
                    queue.append((module, dest, outgoing_pulse))
            else:
                assert False

    return count[0] * count[1]


def solve_part_two(graph, types, initial_state, initial_parents) -> int:
    state = copy.deepcopy(initial_state)
    parents = copy.deepcopy(initial_parents)
    first = {}

    for button_presses in itertools.count():
        queue = collections.deque([(None, "broadcaster", 0)])

        while queue:
            parent, module, pulse = queue.popleft()
            if module == 'vr' and pulse and parent not in first:
                first[parent] = button_presses + 1
                if len(first) == len(parents['vr']):
                    return math.lcm(*first.values())
            if module not in types:
                continue

            if module == "broadcaster":
                for dest in graph[module]:
                    queue.append((module, dest, pulse))
            elif types[module] == '%':
                if pulse:
                    continue
                state[module] = not state[module]
                for dest in graph[module]:
                    queue.append((module, dest, state[module]))
            elif types[module] == '&':
                parents[module][parent] = pulse
                outgoing_pulse = not all(parents[module].values())
                for dest in graph[module]:
                    queue.append((module, dest, outgoing_pulse))
            else:
                assert False

    assert False


def test():
    graph, types, state, parents = read_and_parse("example-1.txt")
    part_one_answer = solve_part_one(graph, types, state, parents)
    assert part_one_answer == 32_000_000

    graph, types, state, parents = read_and_parse("example-2.txt")
    part_one_answer = solve_part_one(graph, types, state, parents)
    assert part_one_answer == 11_687_500


def main():
    graph, types, state, parents = read_and_parse("input.txt")
    part_one_answer = solve_part_one(graph, types, state, parents)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(graph, types, state, parents)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
