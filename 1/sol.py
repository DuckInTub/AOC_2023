import re
from collections import defaultdict

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret

with open("input.txt", "r") as file:
    data = file.read().splitlines()

str_to_num = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine" : 9,
}
str_to_num = keydefaultdict(lambda x : int(x), str_to_num)

matches = [re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", s) for s in data] 
print(matches)

ret = []
for match in matches:
    if len(match) > 1:
        first, last = match[0], match[-1]
        first, last = str_to_num[first], str_to_num[last]
        ret.append(10*first+last)
    else:
        num = str_to_num[match[0]]
        ret.append(10*num+num)

print(ret)
print(sum(ret))
