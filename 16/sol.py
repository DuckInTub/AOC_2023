from collections import deque
from multiprocessing import Pool

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def add_points(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return r1+r2, c1+c2

def energized(array, st, fc):
    points = set()
    seen = set()
    Q = deque()
    Q.append((st, fc))

    while Q:
        at, facing = Q.popleft()
        r, c = at
        if not (0 <= c < len(array[0]) and 0 <= r < len(array)):
            continue
        if (at, facing) in seen:
            continue
        seen.add((at, facing))
        points.add(at)

        ch = array[r][c]
        if ch == ".":
            Q.append((add_points(at, facing), facing))
            continue

        if ch == "\\":
            dr, dc = facing
            new_fc = (dc, dr)
            new_at = add_points(at, new_fc)
            Q.append((new_at, new_fc))
            continue

        if ch == "/":
            dr, dc = facing
            new_fc = (-dc, -dr)
            new_at = add_points(at, new_fc)
            Q.append((new_at, new_fc))
            continue
        
        if ch == "|" and facing in [RIGHT, LEFT]:
            Q.append((add_points(at, UP), UP))
            Q.append((add_points(at, DOWN), DOWN))
            continue

        if ch == "-" and facing in [UP, DOWN]:
            Q.append((add_points(at, LEFT), LEFT))
            Q.append((add_points(at, RIGHT), RIGHT))
            continue
        
        Q.append((add_points(at, facing), facing))
    
    return len(points)


def show(points, array):
    maxC, maxR = len(array[0]), len(array)
    img = []
    for r in range(maxR):
        row = []
        for c in range(maxC):
            # if array[r][c] != ".":
            #     row.append(array[r][c])
            if (r, c) in points:
                row.append("#")
            else:
                row.append(".")
        img.append(row)
    
    return img

with open(0) as file:
    DATA = file.read().splitlines()

p1 = energized(DATA, (0, 0), RIGHT)
print(f"Part 1: {p1}")

start_confs = set()
for c in range(len(DATA[0])):
    start_confs.add(((0, c), DOWN))
    start_confs.add(((len(DATA)-1, c), UP))

for r in range(len(DATA)):
    start_confs.add(((r, 0), RIGHT))
    start_confs.add(((r, len(DATA[0])-1), LEFT))

start_confs = [(DATA, st, fc) for st, fc in start_confs]
with Pool(8) as pool:
    mx = max(pool.starmap(energized, start_confs))

print(f"Part 2: {mx}")