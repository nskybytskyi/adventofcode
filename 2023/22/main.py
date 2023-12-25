#!/usr/bin/env python3
"""Sand Slabs"""
import collections
import operator


def read_and_parse(filename: str) -> list[list[int]]:
    """parse bricks as 6-'tuples' of ints"""
    with open(filename, "r", encoding="utf-8") as file:
        return [list(map(int, line.replace('~', ',').split(',')))
                for line in file.read().splitlines()]


def build_graphs(bricks: list[list[int]]) -> tuple[list[list[int]], list[set[int]]]:
    """find prerequisite bricks of each brick"""
    bricks.sort(key=operator.itemgetter(2))
    num_bricks = ground_id = len(bricks)

    heightmap = collections.defaultdict(lambda: (0, ground_id))
    children = [[] for _ in range(num_bricks + 1)]
    parents = [{ground_id} for _ in range(num_bricks)]

    for brick_id, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        max_height = 0
        surface = [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]

        for x, y in surface:
            height, parent_id = heightmap[x, y]
            if max_height < height:
                max_height = height
                parents[brick_id] = {parent_id}
            elif max_height == height:
                parents[brick_id].add(parent_id)

        for parent_id in parents[brick_id]:
            children[parent_id].append(brick_id)

        for x, y in surface:
            heightmap[x, y] = max_height + z2 - z1 + 1, brick_id

    return children, parents


def solve_part_one(bricks: list[list[int]]) -> int:
    """count bricks that are safe to disintegrate"""
    num_bricks = len(bricks)
    children, parents = build_graphs(bricks)
    unsafe = sum(1 for brick_children in children
                 if any(len(parents[child]) == 1 for child in brick_children))
    return num_bricks + 1 - unsafe


def solve_part_two(bricks: list[list[int]]) -> int:
    """sum up `calc` over all bricks"""
    num_bricks = len(bricks)
    children, parents = build_graphs(bricks)

    def calc(src: int) -> int:
        """count bricks that will fall if src is disintegrated"""
        ans = 0
        cnt = [0] * num_bricks
        bfs = collections.deque([src])

        while bfs:
            brick_id = bfs.popleft()

            for child_id in children[brick_id]:
                cnt[child_id] += 1
                if cnt[child_id] == len(parents[child_id]):
                    ans += 1
                    bfs.append(child_id)

        return ans

    return sum(map(calc, range(num_bricks)))


def test():
    a = read_and_parse("example.txt")
    part_one_answer = solve_part_one(a)
    assert part_one_answer == 5
    part_two_answer = solve_part_two(a)
    assert part_two_answer == 7


def main():
    bricks = read_and_parse("input.txt")
    part_one_answer = solve_part_one(bricks)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(bricks)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
