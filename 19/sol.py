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

# NOTE: Part2 recursively map over intervals of possible values in parts.
# p2 = None
# print(f"Part 2: {p2}")
