import re
from collections import defaultdict

def loop_insts(insts):
    i = 0
    while True:
        yield insts[i]
        i += 1
        if i >= len(insts):
            i = 0

with open("input.txt", "r") as file:
    data = file.read().splitlines()
    insts = data[0]
    MAP = data[2:]

edges = defaultdict(dict)
for line in MAP:
    at, left, right = re.findall(r"\w+", line)
    edges[at]["L"] = left
    edges[at]["R"] = right

starts = [a[:3] for a in MAP if a[2] == "A"]
starts_loop = defaultdict(list)

print(starts)

for start in starts:
    at = start
    i = 0
    inst_generator = loop_insts(insts)
    while len(starts_loop[start]) < 3:
        inst = next(inst_generator)
        at = edges[at][inst]
        i += 1
        if at[-1] == "Z":
            starts_loop[start].append(i)

diffs = []
for loop_values in starts_loop.values():
    first, second, third = loop_values
    diff = second-first
    assert diff == third - second, "Uh oh"
    diffs.append(diff)

from math import lcm
print(lcm(*diffs))
