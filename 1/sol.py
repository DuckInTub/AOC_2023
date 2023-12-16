import re
from collections import defaultdict

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret

with open(0) as file:
    data = file.read().splitlines()

score = 0
for item in [re.findall(r"\d", s) for s in data]:
    first, last = item[0], item[-1]
    score += int(first + last)

print(score)

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

score = 0
for item in matches:
    first, last = str_to_num[item[0]], str_to_num[item[-1]]
    score += 10*first + last

print(score)