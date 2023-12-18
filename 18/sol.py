UP = (0, 1)
RIGHT = (1, 0)
DOWN = (0, -1)
LEFT = (-1, 0)
DIRS = [UP, RIGHT, DOWN, LEFT]

def add_points(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return r1+r2, c1+c2

def mul_point(const, p):
    r, c = p
    return const*r, const*c

def get_corners(insts : list[tuple[int, int]]):
    corners = [(0, 0)]
    at = 0, 0
    for inst in insts:
        direction, step = inst
        step = int(step)
        direction = DIRS["URDL".index(direction)]
        at = add_points(at, mul_point(step, direction))
        corners.append(at)

    return corners

def polygon_area(corners : list[tuple[int, int]]):
    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]

    xs.append(xs[-1])
    ys.append(ys[-1])

    xsum = sum(x*y for x, y in zip(xs, ys[1:] + ys[:1]))
    ysum = sum(x*y for x, y in zip(xs[1:] + xs[:1], ys))

    area = (xsum - ysum) // 2
    assert area == (xsum - ysum) / 2
    return abs(area)

def nr_perimter_points(corners : list[tuple[int, int]]):
    new = list(corners)
    new.append(corners[0])
    length = 0

    for p1, p2 in zip(corners, corners[1:] + corners[:1]):
        x1, y1 = p1
        x2, y2 = p2
        length += abs(y2 - y1) + abs(x2 - x1)
    
    return length

def nr_interior_points(area : int, nr_boundary_points : int):
    """Number of interior points according to pick's theorem"""
    return area - (nr_boundary_points // 2) + 1

with open(0) as file:
    data = file.read().rstrip().splitlines()

corners = get_corners([tuple(inst.split()[:2]) for inst in data])
perimter_points = nr_perimter_points(corners)
area = polygon_area(corners)
p1 = nr_interior_points(area, perimter_points) + perimter_points
print(f"Part 1: {p1}")

hex_insts = [(i.split()[2][2:2+5], i.split()[2][-2]) for i in data]
hex_insts = [("RDLU"[int(d)], int(step, 16)) for step, d in hex_insts]
corners = get_corners(hex_insts)
perimter_points = nr_perimter_points(corners)
area = polygon_area(corners)
p2 = nr_interior_points(area, perimter_points) + perimter_points
print(f"Part 2: {p2}")