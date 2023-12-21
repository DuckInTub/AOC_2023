from collections import deque

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRS = [UP, RIGHT, DOWN, LEFT]

def add_points(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return r1+r2, c1+c2

def move_steps(steps : tuple, start, dim):
    steps = tuple(sorted(steps))
    newQ = deque([start])
    max_r, max_c = dim
    ret = []

    for _ in range(steps[-1]):
        if _ in steps:
            ret.append(set(newQ))
        Q = deque(set(newQ))
        newQ = deque()
        while Q:
            at = Q.pop()

            for d in DIRS:
                new = add_points(at, d)
                nr, nc = new
                if 0 <= nr < max_r and 0 <= nc < max_c and new not in ROCKS:
                    newQ.append(new)
    
    if len(steps) == 1:
        return set(newQ)
    ret.append(set(newQ))
    return ret

def visualize(rocks : set, points : set):
    minR = min(x[0] for x in points.union(rocks))
    maxR = max(x[0] for x in points.union(rocks))
    minC = min(x[1] for x in points.union(rocks))
    maxC = max(x[1] for x in points.union(rocks))

    m = []

    for r in range(minR, maxR):
        row = []
        for c in range(minC, maxC):
            if (r, c) in rocks:
                row.append("#")
            elif (r, c) in points:
                row.append("@")
            else:
                row.append(".")
        m.append(row)

    return list("".join(row) for row in m)

ROCKS = set()
with open(0) as file:
    data = file.read().rstrip().splitlines()
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char == "#":
                ROCKS.add((r, c))
            if char == "S":
                start = (r, c)

dim = (len(data), len(data[0]))
L = dim[0]
relevant_points = move_steps((64, L, L+1), start, dim)
# for row in visualize(ROCKS, p1_points):
#     print(row)

p1 = len(relevant_points[0])
print(f"Part 1: {p1}")

# NOTE For every step we take we expand the possible positions a little,
# We also cycle on a period of 2 which positions are possible, that are not part of the expansion.
# For example the starting square is possible in 2 steps and 4, 6, 8, 10 ... and so on.
# NOTE for the rocks it should be possible to describe their positions with a modulo since,
# we know the size of the map

# NOTE Facts about the input:
# * The first and last column and row are empty
assert len(set(data[0])) == 1
assert len(set(data[-1])) == 1
assert len(set(row[0] for row in data)) == 1
assert len(set(row[-1] for row in data)) == 1

# * The input is square
assert len(set(dim)) == 1
# * The starting row and column are empty
assert "#" not in data[start[0]]

# * We start in the center
assert start == (dim[0] // 2, dim[1] // 2)
# * The diagonal from the center of one edge to the center of another is empty
# TODO, yeah not happening, just, trust me bro...
# * The dimensions of the grid are odd
assert dim[0] % 2 == 1

STEPS = 26501365
nr_even = len(relevant_points[2])
nr_odd = len(relevant_points[1])

# Number of cardinal steps to leave grid:
leave_steps = L // 2 + 1
# Number of odd and even reachable repeated tiles
T = STEPS // L - 1
evens = (T + 1) ** 2
odds  = T ** 2
print("Number of odd: ", nr_odd, "Number of even: ", nr_even)
# Number of steps we can take from the edge on the cardianl edge tiles
rem_steps = (STEPS - leave_steps) % L

c = L // 2 # center of tile
# T R B L
starts = [(L-1, c), (c, 0), (0, c), (c, L-1)]
cardinal_edge_points = list(len(move_steps((rem_steps,), s, dim)) for s in starts)
print("Cardinal edge: ", sum(cardinal_edge_points))

rem_steps -= leave_steps
# TR, BR, BL, TL
starts = [(L-1, 0), (0, 0), (0, L-1), (L-1, L-1)]
triangle_edge_points = list(len(move_steps((rem_steps,), s, dim)) for s in starts)
print("Triangle edge: ", sum(triangle_edge_points))

rem_steps += L
# TR, BR, BL, TL
starts = [(L-1, 0), (0, 0), (0, L-1), (L-1, L-1)]
fold_edge_points = list(len(move_steps((rem_steps,), s, dim)) for s in starts)
print("Fold edge: ", sum(fold_edge_points))

p2 = nr_even * evens + odds * nr_odd
p2 += sum(cardinal_edge_points)
p2 += (T+1)*sum(triangle_edge_points)
p2 += T*sum(fold_edge_points)
print(f"Part 2: {p2}")