import re
from collections import defaultdict

def loop_insts(insts):
    i = 0
    while True:
        yield insts[i]
        i += 1
        if i >= len(insts):
            i = 0

with open(0) as file:
    data = file.read().splitlines()
    insts = data[0]
    MAP = data[2:]

edges = defaultdict(dict)
for line in MAP:
    at, left, right = re.findall(r"\w+", line)
    edges[at]["L"] = left
    edges[at]["R"] = right

insts = loop_insts(insts)
i = 0
at = "AAA"
while at != "ZZZ":
    inst = next(insts)
    at = edges[at][inst]
    i += 1

print(i)

