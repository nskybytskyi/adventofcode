#!/usr/bin/env python3
import collections
import copy
import math

def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        rules, parts = file.read().split('\n\n')
        return rules.split('\n'), parts.split('\n')


def parse_rules(rules):
    mp = {}
    for rule in rules:
        name, steps = rule.split('{')
        mp[name] = []
        for step in steps[:-1].split(','):
            if ':' in step:
                mp[name].append(step.split(':'))
            else:
                mp[name].append(('True', step))
    return mp


def solve_part_one(rules, parts) -> int:
    mp = parse_rules(rules)

    ans = 0
    for part in parts:
        x, m, a, s = [int(chunk[2:]) for chunk in part[1:-1].split(',')]
        rule = 'in'
        while rule not in 'AR':
            for step, dest in mp[rule]:
                if eval(step):
                    rule = dest
                    break
        if rule == 'A':
            ans += x + m + a + s
    return ans


class Block:
    def __init__(self, mnx, mxx, mnm, mxm, mna, mxa, mns, mxs):
        self.mn = {}
        self.mx = {}
        self.mn['x'], self.mx['x'] = mnx, mxx
        self.mn['m'], self.mx['m'] = mnm, mxm
        self.mn['a'], self.mx['a'] = mna, mxa
        self.mn['s'], self.mx['s'] = mns, mxs

    def split(self, step):
        if step == 'True':
            return self, Block(0, -1, 0, -1, 0, -1, 0, -1)
        var, sign, *val = step
        val = int(''.join(val))
        if sign == '>':
            good, bad = copy.deepcopy(self), copy.deepcopy(self)
            good.mn[var] = max(good.mn[var], val + 1)
            bad.mx[var] = min(bad.mx[var], val)
            return good, bad
        else:
            good, bad = copy.deepcopy(self), copy.deepcopy(self)
            good.mx[var] = min(good.mx[var], val - 1)
            bad.mn[var] = max(bad.mn[var], val)
            return good, bad
    
    def __bool__(self):
        return self.size() > 0

    def size(self):
        return math.prod((self.mx[c] - self.mn[c] + 1) for c in 'xmas')


def solve_part_two(rules) -> int:
    ans = 0
    mp = parse_rules(rules)
    q = collections.deque([('in', Block(1, 4_000, 1, 4_000, 1, 4_000, 1, 4_000))])
    while q:
        rule, block = q.popleft()
        if rule == 'A':
            ans += block.size()
        elif rule != 'R':
            for step, dest in mp[rule]:
                good, block = block.split(step)
                if good:
                    q.append((dest, good))
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
