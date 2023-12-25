#!/usr/bin/env python3
def read_and_parse(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as file:
        return list(map(list, file.read().splitlines()))


def solve_part_one(a) -> int:
    pass


def solve_part_two(a) -> str:
    pass


def test():
    pass


def main():
    a = read_and_parse("input.txt")
    part_one_answer = solve_part_one(a)
    print(f"Part One: {part_one_answer}")
    part_two_answer = solve_part_two(a)
    print(f"Part Two: {part_two_answer}")


if __name__ == "__main__":
    test()
    main()
