from itertools import combinations, product

def sign(x):
    return round(x / abs(x))

def get_line(string : str):
    x, y, _, dx, dy, _ = tuple(int(x) for x in string.replace("@", ",").replace(",", "").split())
    k = dy / dx
    m = y - k*x
    sx = sign(dx)
    sy = sign(dy)
    return (x, y, sx, sy, k, m)

def intersect(l1, l2):
    x1, y1, sx1, sy1, a, c = l1
    x2, y2, sx2, sy2, b, d = l2
    if a == b:
        return False
    x = (d - c) / (a - b)
    y = a*x + c
    if sign(x - x1) == sx1 and sign(x - x2) == sx2:
        if sign(y - y1) == sy1 and sign(y - y2) == sy2:
            return (x, y)
    return False

with open(0) as file:
    data = file.read().rstrip().splitlines()

BOUNDS = (200000000000000, 400000000000000)
# BOUNDS = (7, 27)
p1 = 0
for line1, line2 in combinations(data, 2):
    l1, l2 = get_line(line1), get_line(line2)
    if not intersect(l1, l2):
        continue
    x, y = intersect(l1, l2)
    if BOUNDS[0] <= x <= BOUNDS[1] and BOUNDS[0] <= y <= BOUNDS[1]:
        p1 += 1

print(f"Part 1: {p1}")
# p2 = None
# print(f"Part 2: {p2}")
