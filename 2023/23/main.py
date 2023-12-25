#!/usr/bin/env python3
import sys
import collections
sys.setrecursionlimit(100_000)


def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def solve_part_one(a) -> int:
    R, C = len(a), len(a[0])
    # path = [(0, 1)]
    seen = {(0, 1)}

    def nei(r, c):
        if a[r][c] == '.':
            return [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
        return {'^': [(r - 1, c)], '<': [(r, c - 1)],
                '>': [(r, c + 1)], 'v': [(r + 1, c)]}[a[r][c]]

    mx = 0

    def backtrack(r, c):
        nonlocal mx
        if r == R - 1 and c == C - 2:
            mx = max(mx, len(seen))

        for nr, nc in nei(r, c):
            if (
                0 <= nr < R and 0 <= nc < C and 
                a[nr][nc] != '#' and (nr, nc) not in seen
            ):
                # path.append((nr, nc))
                seen.add((nr, nc))
                backtrack(nr, nc)
                seen.remove((nr, nc))

    backtrack(0, 1)
    return mx - 1


def solve_part_two(a) -> int:
    R, C = len(a), len(a[0])
    g = collections.defaultdict(list)

    for r in range(R):
        for c in range(C):
            if a[r][c] == '#':
                continue
            for nr, nc in (r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c):
                if 0 <= nr < R and 0 <= nc < C and a[nr][nc] != '#':
                    g[r, c].append((nr, nc))

    special = {(0, 1), (R - 1, C - 2)}
    for r in range(R):
        for c in range(C):
            if len(g[r, c]) > 2:
                special.add((r, c))

    gg = collections.defaultdict(lambda: collections.defaultdict(int))
    for sr, sc in special:
        d = {(sr, sc): 0}
        q = collections.deque([(sr, sc)])
        while q:
            r, c = q.popleft()
            for nr, nc in (r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c):
                if 0 <= nr < R and 0 <= nc < C and a[nr][nc] != '#' and (nr, nc) not in d:
                    if (nr, nc) in special:
                        gg[sr, sc][nr, nc] = max(gg[sr, sc][nr, nc], d[r, c] + 1)
                    else:
                        d[nr, nc] = d[r, c] + 1
                        q.append((nr, nc))

    mx = 0
    seen = {(0, 1)}
    length = 0

    def backtrack(v):
        nonlocal mx, length
        if v == (R - 1, C - 2):
            mx = max(mx, length)

        for u, w in gg[v].items():
            if u in seen:
                continue
            length += w
            seen.add(u)
            backtrack(u)
            seen.remove(u)
            length -= w

    backtrack((0, 1))
    return mx


def test():
    a = read_and_parse("example.txt")
    part_one_answer = solve_part_one(a)
    assert part_one_answer == 94
    part_two_answer = solve_part_two(a)
    assert part_two_answer == 154


def main():
    a = read_and_parse("input.txt")
    part_one_answer = solve_part_one(a)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(a)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
