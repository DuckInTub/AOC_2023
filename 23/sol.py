from collections import deque
from typing import Dict, Tuple

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
def add_points(p1, p2):
    return tuple(x+y for x, y in zip(p1, p2))

def find_intersections():
    points = set()
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char != ".":
                continue
            total = 0
            for d in DIRS:
                new = add_points((r, c), d)
                nr, nc = new
                if not (0 <= nr < len(data) and 0 <= nc < len(data[0])):
                    continue
                if data[nr][nc] != '#':
                    total += 1
            if total >= 3:
                points.add((r, c))
    return points

def next_intersection_dist(start, intersections, slipp=False):
    seen = set()
    Q = deque([(0, start)])
    dists = {}
    while Q:
        steps, at = Q.pop()
        if at in seen:
            continue
        seen.add(at)
        if at in intersections - {start}:
            dists[at] = steps
            continue

        for d in DIRS:
            new = add_points(d, at)
            nr, nc = new
            if not (0 <= nr < len(data) and 0 < nc <= len(data[0])):
                continue
            if slipp and data[nr][nc] in "^>v<":
                forced_d = DIRS["^>v<".index(data[nr][nc])]
                if d != forced_d:
                    continue
            if new not in seen and data[nr][nc] != '#':
                Q.append((steps+1, new))
    
    return dists

def longest_path(start, stop, graph : Dict[Tuple[int, int], Dict[Tuple[int, int], int]]):
    seen = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
    def dfs(curr):
        if curr == stop:
            return 0
        mx = 0
        for new, dist in graph[curr].items():
            nr, nc = new
            if not seen[nr][nc]:
                seen[nr][nc] = True
                mx = max(mx, dfs(new)+dist)
                seen[nr][nc] = False
        return mx
    
    return dfs(start)

with open(0) as file:
    data = file.read().rstrip().splitlines()
    START = (0, data[0].index("."))
    STOP  = (len(data)-1, data[-1].index("."))

intersections = find_intersections().union({START, STOP})
GRAPH = dict()
SLIPP_GRAPH = dict()
for crossing in intersections:
    slipp = next_intersection_dist(crossing, intersections, slipp=True)
    SLIPP_GRAPH[crossing] = slipp
    dists = next_intersection_dist(crossing, intersections)
    GRAPH[crossing] = dists

p1 = longest_path(START, STOP, SLIPP_GRAPH)
print(f"Part 1: {p1}")

p2 = longest_path(START, STOP, GRAPH)
print(f"Part 2: {p2}")