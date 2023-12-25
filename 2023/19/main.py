#!/usr/bin/env python3
"""Aplenty"""
import collections
import copy
import math


def read_and_parse(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r", encoding="utf-8") as file:
        rules, parts = file.read().split('\n\n')
        return rules.split('\n'), parts.split('\n')


def parse_rules(rules):
    mapping = {}
    for rule in rules:
        name, steps = rule.split('{')
        mapping[name] = []
        for step in steps[:-1].split(','):
            if ':' in step:
                mapping[name].append(step.split(':'))
            else:
                mapping[name].append(('True', step))
    return mapping


def solve_part_one(rules, parts) -> int:
    mapping = parse_rules(rules)

    def parse_part(raw: str) -> dict[str, int]:
        return {chunk[0]: int(chunk[2:]) for chunk in raw[1:-1].split(',')}

    def safe_eval(step: str, part: dict[str, int]) -> bool:
        if step == 'True':
            return True

        if step[1] == '>':
            return part[step[0]] > int(step[2:])
        return part[step[0]] < int(step[2:])

    ans = 0
    for part in map(parse_part, parts):
        rule = 'in'
        while rule not in 'AR':
            for step, dest in mapping[rule]:
                if safe_eval(step, part):
                    rule = dest
                    break
        if rule == 'A':
            ans += sum(part.values())
    return ans


class Block:
    """4d range of parts"""
    def __init__(self, *args):
        mnx, mxx, mnm, mxm, mna, mxa, mns, mxs = args
        self.lower_bound = {}
        self.upper_bound = {}
        self.lower_bound['x'], self.upper_bound['x'] = mnx, mxx
        self.lower_bound['m'], self.upper_bound['m'] = mnm, mxm
        self.lower_bound['a'], self.upper_bound['a'] = mna, mxa
        self.lower_bound['s'], self.upper_bound['s'] = mns, mxs

    def split(self, step):
        if step == 'True':
            return self, Block(0, -1, 0, -1, 0, -1, 0, -1)
        var, sign, *val = step
        val = int(''.join(val))

        if sign == '>':
            good, bad = copy.deepcopy(self), copy.deepcopy(self)
            good.lower_bound[var] = max(good.lower_bound[var], val + 1)
            bad.upper_bound[var] = min(bad.upper_bound[var], val)
            return good, bad

        good, bad = copy.deepcopy(self), copy.deepcopy(self)
        good.upper_bound[var] = min(good.upper_bound[var], val - 1)
        bad.lower_bound[var] = max(bad.lower_bound[var], val)
        return good, bad

    def __bool__(self):
        return self.size() > 0

    def size(self):
        return math.prod((self.upper_bound[c] - self.lower_bound[c] + 1) for c in 'xmas')


def solve_part_two(rules) -> int:
    ans = 0
    mapping = parse_rules(rules)
    queue = collections.deque([('in', Block(1, 4_000, 1, 4_000, 1, 4_000, 1, 4_000))])
    while queue:
        rule, block = queue.popleft()
        if rule == 'A':
            ans += block.size()
        elif rule != 'R':
            for step, dest in mapping[rule]:
                good, block = block.split(step)
                if good:
                    queue.append((dest, good))
    return ans


def test():
    rules, parts = read_and_parse("example.txt")
    part_one_answer = solve_part_one(rules, parts)
    assert part_one_answer == 19_114
    part_two_answer = solve_part_two(rules)
    assert part_two_answer == 167_409_079_868_000


def main():
    rules, parts = read_and_parse("input.txt")
    part_one_answer = solve_part_one(rules, parts)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(rules)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
