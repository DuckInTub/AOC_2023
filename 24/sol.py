from itertools import combinations, product
from math import sqrt
import numpy as np

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

def parse(line):
    x, y, z, dx, dy, dz = tuple(int(x) for x in line.replace("@", ",").split(","))
    return (x, y, z), (dx, dy, dz)

def norm(vec):
    x, y, z = vec
    L = sqrt(x ** 2 + y ** 2 + z ** 2)
    return tuple(c / L for c in vec)

def sub(v1, v2):
    return tuple(c1 - c2 for c1, c2 in zip(v1, v2))

# The rock we throws starting position P and its velocity V
# Needs to be able to form euqations P+N*V = H + N*HV
# For all hail stones H with velocity HV
# such that N is an positive integer.
pairs = []
for line1, line2 in combinations(data, 2):
    (_, _, _), (x, y, z) = parse(line1)
    (_, _, _), (dx, dy, dz) = parse(line2)
    n1 = norm((x, y, z))
    n2 = norm((dx, dy, dz))
    if all(abs(c) < 0.0001 for c in sub(n1, n2)):
        pairs.append((line1, line2))
        print(n1)
        print(n2)
        print(f"Line 1: {line1}, Line 2: {line2}")
        print()
    
print(len(pairs))
print("--------Part 2---------")

use = data[:3]
best = (0, 0, 0)
mn = 10 ** 50
best_sol = [10 ** 8]*2*len(use)
for vx in range(312-25, 312+25, 1):
    for vy in range(-116-25, -116+25, 1):
        for vz in range(109-25, 109+25, 1):
            # vx, vy, vz = -3, 1, 2
            rows = []
            consts = []
            L = 3*len(use)
            for i in range(len(use)):
                (x, y, z), (dx, dy, dz) = parse(use[i])

                row = [0]*(3+len(use))
                row[0] = 1
                row[3+i] = vx-dx
                consts.append(x)
                rows.append(row)

                row = [0]*(3+len(use))
                row[1] = 1
                row[3+i] = vy-dy
                consts.append(y)
                rows.append(row)

                row = [0]*(3+len(use))
                row[2] = 1
                row[3+i] = vz-dz
                consts.append(z)
                rows.append(row)
            
            mat = np.array(rows)
            consts = np.array(consts)
            try:
                sol_pos, *rest = np.linalg.lstsq(mat, consts, rcond=1)
                thing = rest[0][0]
            except np.linalg.LinAlgError as e:
                continue
            if thing < mn:
                best_sol = sol_pos
                print(rest)
                best = (vx, vy, vz)
                print(best)
                mn = thing
                print(thing)

print("------------------------")
print("Min error: ", mn)
print(best)
print([float(x) for x in best_sol[:3]])
# p2 = None
# print(f"Part 2: {p2}")
vx, vy, vz = (312, -116, 109)
rows = []
consts = []
L = 3*len(use)
for i in range(len(use)):
    (x, y, z), (dx, dy, dz) = parse(use[i])

    row = [0]*(3+len(use))
    row[0] = 1
    row[3+i] = vx-dx
    consts.append(x)
    rows.append(row)

    row = [0]*(3+len(use))
    row[1] = 1
    row[3+i] = vy-dy
    consts.append(y)
    rows.append(row)

    row = [0]*(3+len(use))
    row[2] = 1
    row[3+i] = vz-dz
    consts.append(z)
    rows.append(row)

mat = np.array([row[:5] for row in rows][:5])
print(mat)
consts = np.array(consts[:5])
sol = np.linalg.solve(mat, consts)
sol = [float(x) for x in sol[:3]]
assert all(int(x) == x for x in sol)
print(sum([int(x) for x in sol[:3]]))