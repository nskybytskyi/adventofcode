#!/usr/bin/env python3
"""Aplenty"""
import collections
import copy
import math
from typing import Iterable


Part = dict[str, int]
Block = dict[str, range]


def parse_part(raw: str) -> Part:
    return {chunk[0]: int(chunk[2:]) for chunk in raw[1:-1].split(",")}


class Rule:
    """a singular rule like x>10"""

    __OPERATORS = {
        ">": int.__gt__,
        "<": int.__lt__,
    }

    def __init__(self, raw: str):
        self.name = raw[0]
        self.sign = raw[1]
        self.value = int(raw[2:])

    def apply_to_part(self, part: Part) -> bool:
        return Rule.__OPERATORS[self.sign](part[self.name], self.value)

    def apply_to_block(self, block: Block) -> tuple[Block, Block]:
        result = copy.deepcopy(block)
        in_ref, out_ref = block[self.name], result[self.name]

        if self.sign == ">":
            block[self.name] = range(in_ref.start, min(self.value + 1, in_ref.stop))
            result[self.name] = range(max(out_ref.start, self.value + 1), out_ref.stop)
        else:
            block[self.name] = range(max(in_ref.start, self.value), in_ref.stop)
            result[self.name] = range(out_ref.start, min(self.value, out_ref.stop))

        return result, block


class Workflow:
    """a named collection of rules with destinations"""

    def __init__(self, raw: str):
        self.name, rest = raw.split("{")
        self.rules, self.destinations = [], []
        *steps, final = rest[:-1].split(",")

        for step in steps:
            raw_rule, destination = step.split(":")
            self.rules.append(Rule(raw_rule))
            self.destinations.append(destination)

        self.destinations.append(final)

    def apply_to_part(self, part: Part) -> str:
        for rule, destination in zip(self.rules, self.destinations):
            if rule.apply_to_part(part):
                return destination
        return self.destinations[-1]

    def apply_to_block(self, block: Block) -> Iterable[tuple[str, Block]]:
        for rule, destination in zip(self.rules, self.destinations):
            result, block = rule.apply_to_block(block)
            yield destination, result
        yield self.destinations[-1], block


def read_and_parse(filename: str) -> tuple[list[Workflow], list[Part]]:
    with open(filename, "r", encoding="utf-8") as file:
        raw_workflows, raw_parts = file.read().split("\n\n")
        workflows = list(map(Workflow, raw_workflows.split("\n")))
        parts = list(map(parse_part, raw_parts.split("\n")))
        return workflows, parts


def solve_part_one(workflows: list[Workflow], parts: list[Part]) -> int:
    mapping = {workflow.name: workflow for workflow in workflows}

    total = 0
    for part in parts:
        name = "in"
        while name not in "AR":
            name = mapping[name].apply_to_part(part)
        if name == "A":
            total += sum(part.values())
    return total


def solve_part_two(workflows: list[Workflow]) -> int:
    mapping = {workflow.name: workflow for workflow in workflows}

    total = 0
    queue = collections.deque([(str("in"), {key: range(1, 4001) for key in "xmas"})])
    while queue:
        name, block = queue.popleft()
        if name == "A":
            total += math.prod(map(len, block.values()))
        elif name != "R":
            queue.extend(mapping[name].apply_to_block(block))
    return total


def test():
    workflows, parts = read_and_parse("example.txt")
    part_one_answer = solve_part_one(workflows, parts)
    assert part_one_answer == 19_114
    part_two_answer = solve_part_two(workflows)
    assert part_two_answer == 167_409_079_868_000


def main():
    workflows, parts = read_and_parse("input.txt")
    part_one_answer = solve_part_one(workflows, parts)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(workflows)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
