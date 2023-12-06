from math import ceil, floor, sqrt
import re

def pq(p, q):
    D = -p / 2
    Q = sqrt(D ** 2 - q)
    return (D + Q, D - Q)

with open("test.txt", "r") as file:
    data = file.read().splitlines()
    times = [int(x) for x in re.findall(r"\d+", data[0])]
    dists = [int(x) for x in re.findall(r"\d+", data[1])]

score = 1
for time, dist in zip(times, dists):
    # Solve the equation x^2 - time*x + dist = 0
    # Which is the same as x * (time - x) > dist
    # whos integers solutions are possible races

    # Gives us a non inclusive range of floats (f1, f2)
    # So turn that in to a incluse range of ints [i1, i2]
    # The number of elements in that range is i2-i1+1
    low, high = sorted(pq(-time, dist))
    low = floor(low+1)
    high = ceil(high-1)
    range_len = high - low + 1
    score *= range_len

print(score)

time = int("".join(str(x) for x in times))
dist = int("".join(str(x) for x in dists))
print(time, dist)
low, high = sorted(pq(-time, dist))
low = floor(low+1)
high = ceil(high-1)
range_len = high - low + 1

print(range_len)