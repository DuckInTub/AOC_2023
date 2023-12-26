from itertools import combinations, pairwise

def sign(x):
    if x == 0:
        return 0
    return round(x / abs(x))

def parse(line):
    x, y, z, dx, dy, dz = tuple(int(x) for x in line.replace("@", ",").split(","))
    return (x, y, z), (dx, dy, dz)

def ray_intersect_2d(line1, line2):
    (x1, y1, _), (dx1, dy1, _) = line1
    (x2, y2, _), (dx2, dy2, _) = line2
    if dx1 == 0 or dx2 == 0:
        return False
    k1 = dy1 / dx1
    k2 = dy2 / dx2
    m1 = y1 - k1*x1
    m2 = y2 - k2*x2
    if k1 == k2:
        return False
    x = (m2 - m1) / (k1 - k2)
    y = k1*x + m1
    if sign(x - x1) == sign(dx1) and sign(x - x2) == sign(dx2) and sign(y - y1) == sign(dy1) and sign(y - y2) == sign(dy2):
        return (x, y)
    return False

def add_point(p1, p2):
    return tuple(c1 + c2 for c1, c2 in zip(p1, p2))

def sub_points(p1, p2):
    return tuple(c1 - c2 for c1, c2 in zip(p1, p2))

def mul_point(c, p1):
    return tuple(c*c1 for c1 in p1)

def alternating(x):
    for i in range(x):
        yield i
        yield -i

with open(0) as file:
    data = file.read().rstrip().splitlines()

BOUNDS = (200000000000000, 400000000000000)
p1 = 0
for line1, line2 in combinations(data, 2):
    (x1, y1, _), (dx1, dy1, _) = parse(line1)
    (x2, y2, _), (dx2, dy2, _) = parse(line2)
    if (xy := ray_intersect_2d(parse(line1), parse(line2))):
        x, y = xy
        if BOUNDS[0] <= x <= BOUNDS[1] and BOUNDS[0] <= y <= BOUNDS[1]:
            p1 += 1

print(f"Part 1: {p1}")

def get_XY():
    mn = 10 ** 8
    for vx in alternating(500):
        for vy in alternating(500):
            good = True
            intersections = []
            line1 = data[0]
            for line2 in data[1:]:
                (x1, y1, _), (dx1, dy1, _) = parse(line1)
                (x2, y2, _), (dx2, dy2, _) = parse(line2)
                dx1, dy1 = dx1-vx, dy1-vy
                dx2, dy2 = dx2-vx, dy2-vy
                intersect = ray_intersect_2d(((x1, y1, 0), (dx1, dy1, 0)), ((x2, y2, 0), (dx2, dy2, 0)))
                if not intersect:
                    good = False
                    break
                intersections.append(intersect)
            
            if good:
                err = sum(abs(x) for x, _ in [(sub_points(p1, p2)) for p1, p2 in pairwise(intersections)])
                err_arr = [abs(x) for x, _ in [(sub_points(p1, p2)) for p1, p2 in pairwise(intersections)]]
                if err <= mn:
                    print(err_arr)
                    print(err)
                    mn = err
                    intersections.sort(key=lambda x : (x[0]-int(x[0]), x[1]-int(x[1])))
                    px, py = intersections[0]
                    bvx, bvy = vx, vy
                    if err == 0:
                        return (px, py), (vx, vy)

    return (px, py), (bvx, bvy)

(p_x, p_y), (bvx, bvy) = get_XY()
print(bvx, bvy)
print(p_x, p_y)
assert int(p_x) == p_x and int(p_y) == p_y
p_x, p_y = int(p_x), int(p_y)

# From here we have two unknowns:
# The Z of the starting position
# The Z of the velocity
# These can easily be found by solving
# a system of linear equations!

eqs = []
for i, line in enumerate(data[:2]):
    (x1, y1, z1), (dx1, dy1, dz1) = parse(line)
    N1 = (p_x - x1) / (dx1 - bvx)
    # assert N1 == (p_y - y1) / (dy1 - bvy)
    hit_rock = add_point((x1, y1, z1), mul_point(N1, (dx1, dy1, dz1)))
    print(f"{i}. Z + {N1}*V = {hit_rock[-1]}")
    eqs.append((N1, hit_rock[-1]))

C1, S1 = eqs[0]
C2, S2 = eqs[1]
#  Z + C1*V = S1
#  Z + C2*V = S2
#  C1*V - C2*V = S1 - S2
#  V*(C1 - C2) = S1 - S2
#  V = (S1 - S2) / (C1 - C2)
#  Z = S1 - C1*V
vz = (S1 - S2) / (C1 - C2)
p_z = S1 - C1*vz

print(f"Start at {(p_x, p_y, int(p_z))}")
print(f"With velocity {(bvx, bvy, vz)}")
S = sum((p_x, p_y, p_z))
assert int(S) == S
print(f"Part 2: {int(S)}")