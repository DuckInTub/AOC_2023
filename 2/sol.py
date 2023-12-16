from math import prod
import re

allowed = {'r' : 12, 'g' : 13, 'b' : 14}

with open(0) as file:
    data = file.read().splitlines()

possible = []
counts = []
for i, line in enumerate(data):
    matches = re.findall(r"(\d+ [a-z])", line)
    ok = True
    count =  {'r' : 0, 'g' : 0, 'b' : 0}
    for item in matches:
        num, c = item.split()
        num = int(num)
        count[c] = max(count[c], num)
        if num > allowed[c]:
            ok = False
    if ok:
        possible.append(i+1)
    counts.append(count)
        
print(sum(possible))
score = sum(prod(count.values()) for count in counts)
print(score)