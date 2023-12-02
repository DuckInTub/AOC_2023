from math import prod
import re

allowed = {'r' : 12, 'g' : 13, 'b' : 14}

with open("input.txt", "r") as file:
    data = file.read().splitlines()


possible = []

for i, line in enumerate(data):
    thing = re.findall(r"(\d+ [a-z])", line)
    ok = True
    for item in thing:
        num, c = item.split(" ")
        num = int(num)
        if allowed[c] < num:
            ok = False
            break
    if ok:
        possible.append(i+1)
        
print(sum(possible))

counts = []
for i, line in enumerate(data):
    thing = re.findall(r"(\d+ [a-z])", line)
    count =  {'r' : 0, 'g' : 0, 'b' : 0}
    for item in thing:
        num, c = item.split(" ")
        num = int(num)
        count[c] = max(count[c], num)
    counts.append(count)

score = sum(prod(count.values()) for count in counts)
print(score)