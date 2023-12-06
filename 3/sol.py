from collections import defaultdict
from math import prod

SYMBOLS = set()
NUMS = set()
GEARS = set()
with open("input.txt", "r") as file:
    data = file.read().splitlines()
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char.isdigit():
                NUMS.add((r, c))
            elif char != '.':
                SYMBOLS.add((r, c))
            if char == '*':
                GEARS.add((r, c))

valids = []
gear_nums = defaultdict(list)
for r, line in enumerate(data):
    num = 0
    ok = False
    gear = 0
    for c, char in enumerate(line):
        if char.isdigit():
            num = 10*num + int(char)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    cord = r+dr, c+dc
                    if cord in SYMBOLS:
                        ok = True
                    if cord in GEARS:
                        gear = cord
        else:
            if ok:
                valids.append(num)
            if ok and gear:
                gear_nums[gear].append(num)
            num = 0
            ok = False
            gear = 0
    if ok:
        valids.append(num)
    if gear:
        gear_nums[gear].append(num)

p1 = sum(valids)
p2 = sum(prod(nums) for nums in gear_nums.values() if len(nums) == 2)
print(p1, p2)