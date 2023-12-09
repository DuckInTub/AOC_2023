from itertools import pairwise

def get_next(seq):
    if all(x == 0 for x in seq):
        return 0
    return seq[-1] + get_next([p2 - p1 for p1, p2 in pairwise(seq)])

def get_prev(seq):
    if all(x == 0 for x in seq):
        return 0
    return seq[0] - get_prev([p2 - p1 for p1, p2 in pairwise(seq)])

with open("input.txt", "r") as file:
    data = [[int(x) for x in line.split()] for line in file.readlines()]

score = lambda f, d : sum(map(f, d))
print(score(get_next, data))
print(score(get_prev, data))