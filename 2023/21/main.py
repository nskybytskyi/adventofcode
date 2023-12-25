#!/usr/bin/env python3
import collections


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def solve_part_one(a, steps=64) -> int:
    R, C = len(a), len(a[0])
    sr = sc = -1
    for r in range(R):
        for c in range(C):
            if a[r][c] == 'S':
                sr, sc = r, c
    q = [{(sr, sc)}]
    for i in range(steps):
        q.append(set())
        for r, c in q[i]:
            for nr, nc in (r-1,c),(r,c-1),(r,c+1),(r+1,c):
                if 0 <= nr < R and 0 <= nc < C and a[nr][nc] != '#':
                    q[i + 1].add((nr, nc))
    return len(q[steps])


def solve_part_two_naive(a, steps) -> int:
    N = len(a)
    R, C = len(a), len(a[0])
    sr = sc = -1
    for r in range(R):
        for c in range(C):
            if a[r][c] == 'S':
                sr, sc = r, c
    seen = {(sr, sc)}
    total = 0
    q = collections.deque([(sr, sc)])
    for i in range(steps):
        if i % 2 == steps % 2:
            total += len(q)
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in (r-1,c),(r,c-1),(r,c+1),(r+1,c):
                if a[nr % R][nc % C] != '#' and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc))
    return total + len(q)


def solve_part_two(a, steps=26_501_365) -> int:
    N = len(a)
    M = N >> 1

    def key(state):
        r, c, parity = state
        return r % N, c % N, parity, r >= M, c >= M

    s = M, M, 0
    q = collections.deque([s])
    d = {key(s): 0}
    unique = collections.defaultdict(set)
    unique[key(s)].add(s)

    while q:
        old_state = q.popleft()
        old_group = key(old_state)
        r, c, parity = old_state

        for nr, nc in (r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c):
            if a[nr % N][nc % N] == '#':
                continue

            new_state = nr, nc, 1 - parity
            new_group = key(new_state)

            if (
                new_group not in d or (
                    d[new_group] == d[old_group] + 1 and 
                    new_state not in unique[new_group]
                )
            ):
                q.append(new_state)
                d[new_group] = d[old_group] + 1
                unique[new_group].add(new_state)

    total = 0

    for group, distance in d.items():
        r, c, parity, *_ = group
        if parity != steps & 1 or steps < distance:
            continue

        blocks = (steps - distance) // (2 * N) + 1
        if len(unique[group]) == 1:
            total += blocks**2
        elif len(unique[group]) == 2:
            total += blocks * (blocks + 1)
        else:
            assert False

    return total


def test():
    data = read_and_parse("example.txt")
    part_one_answer = solve_part_one(data, 6)
    assert part_one_answer == 16

    part_one_answer = solve_part_two_naive(data, 6)
    assert part_one_answer == 16
    part_two_answer = solve_part_two_naive(data, 10)
    assert part_two_answer == 50
    part_two_answer = solve_part_two_naive(data, 50)
    assert part_two_answer == 1_594
    part_two_answer = solve_part_two_naive(data, 100)
    assert part_two_answer == 6_536
    part_two_answer = solve_part_two_naive(data, 500)
    assert part_two_answer == 167_004
    # part_two_answer = solve_part_two_naive(data, 1000)
    # assert part_two_answer == 668_697
    # part_two_answer = solve_part_two_naive(data, 5000)
    # assert part_two_answer == 16_733_044

    data = read_and_parse("input.txt")
    part_two_answer = solve_part_two(data, 10)
    assert part_two_answer == 103
    part_two_answer = solve_part_two(data, 50)
    assert part_two_answer == 2_272
    part_two_answer = solve_part_two(data, 100)
    assert part_two_answer == 9_102
    part_two_answer = solve_part_two(data, 500)
    assert part_two_answer == 223_017
    part_two_answer = solve_part_two(data, 1000)
    assert part_two_answer == 890_178


def main():
    data = read_and_parse("input.txt")
    part_one_answer = solve_part_one(data)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(data)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
