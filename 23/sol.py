from collections import deque
from copy import deepcopy

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRS = [UP, RIGHT, DOWN, LEFT]

def add_points(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return r1+r2, c1+c2

def longest_path_slip(steps, start, stop, seen):
    at = start
    possible = []
    while True:
        seen.add(at)
        possible = []
        r, c = at
        char = data[r][c]
        assert char != '#'
        if at == START:
            at = add_points(at, DOWN)
            steps += 1
            continue

        if at == STOP:
            return steps

        if char in "^>v<":
            d = DIRS["^>v<".index(char)]
            at = add_points(at, d)
            if at in seen:
                return -1
            steps += 1
            continue

        for d in DIRS:
            new = add_points(at, d)
            nr, nc = new
            if data[nr][nc] != '#' and new not in seen:
                assert data[nr][nc] != '#'
                possible.append(new)
        
        if len(possible) == 1:
            new = possible[0]
            nr, nc = new
            if data[nr][nc] == '#':
                continue
            at = new 
            steps += 1
            continue
    
        mx = 0
        for new in possible:
            nr, nc = new
            if data[nr][nc] != '#':
                mx = max(mx, longest_path_slip(steps+1, new, stop, set(seen)))
        return mx


with open(0) as file:
    data = file.read().rstrip().splitlines()

# for row in data:
#     print(row)

# Find all intersections
# For each intersection find the distance to
# the neighbouring intersections.
# We now have a graph of distances between the intersections
# Use dijkstras algorithm for longest path.

START = (0, data[0].index("."))
STOP  = (len(data)-1, data[-1].index("."))
print(f"START {START}, Stop {STOP}")
p1 = longest_path_slip(0, START, STOP, set())
print(f"Part 1: {p1}")

# p2 = None
# print(f"Part 2: {p2}")
