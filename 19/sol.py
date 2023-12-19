from collections import deque
from copy import deepcopy
from math import prod


class Rule:
    def __init__(self, string : str) -> None:
        i = string.index("{")
        self.name = string[:i]
        rules = string.split(",")
        rules[0] = rules[0][i+1:]
        rules[-1] = rules[-1].replace("}", "")
        self.rules = rules
    
    def apply(self, part):
        for rule in self.rules:
            if ":" in rule:
                r, go = rule.split(":")
                key, value = r[0], int(r[2:])
                if "<" in r:
                    if part[key] < value:
                        return go
                if ">" in r:
                    if part[key] > value:
                        return go
            else:
                return rule
        assert False
    
    def __repr__(self) -> str:
        return f"{self.name}, {self.rules}"

def parse_part(part):
    part = part[1:-1]
    ret = {}
    for thing in part.split(","):
        key, value = thing.split("=")
        ret[key] = int(value)
    return ret

def parse_rule(rule):
    i = rule.index("{")
    name = rule[:i]
    rule = rule[i+1:-1]
    rule = [r for r in rule.split(",")]
    return name, rule

def accepted(rules):
    Q = deque()
    start = {key:(1, 4000) for key in "xmas"}
    Q.append(("in", start))
    nr = 0
    while Q:
        rule_key, ranges = Q.pop()

        if rule_key == "R":
            continue
        if rule_key == "A":
            nr += prod(h-l+1 for l, h in ranges.values())
            continue

        rule = rules[rule_key]
        for part in rule:
            if ":" not in part:
                Q.append((part, deepcopy(ranges)))
                continue
            
            cond, nxt = part.split(":")
            key = cond[0]
            value = int(cond[2:])
            
            if ">" in cond:
                new = deepcopy(ranges)
                low, high = ranges[key]
                new[key] = (max(low, value+1), high)
                Q.append((nxt, new))
                ranges[key] = (low, value)

            if "<" in cond:
                new = deepcopy(ranges)
                low, high = ranges[key]
                new[key] = (low, min(high, value-1))
                Q.append((nxt, new))
                ranges[key] = (value, high)
    
    return nr

with open(0) as file:
    rules_, parts = file.read().rstrip().split("\n\n")
    rules = {}
    for rule in rules_.splitlines():
        rule = Rule(rule)
        rules[rule.name] = rule
    parts = [parse_part(part) for part in parts.splitlines()]

p1 = 0
for part in parts:
    rule_key = "in"
    while rule_key not in ["A", "R"]:
        rule = rules[rule_key]
        rule_key = rule.apply(part)
    if rule_key == "R":
        continue
    if rule_key == "A":
        p1 += sum(v for v in part.values())
        continue
    assert False, "?"

print(f"Part 1: {p1}")

# NOTE: Part 2 map over intervals of possible values in parts.
rules = {parse_rule(r)[0] : parse_rule(r)[1] for r in rules_.splitlines()}
assert "in" in rules
p2 = accepted(rules)
print(f"Part 2: {p2}")