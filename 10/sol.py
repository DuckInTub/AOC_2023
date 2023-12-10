# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

pipes = {
    "|": (UP, DOWN),
    "-": (LEFT, RIGHT),
    "L": (UP, RIGHT),
    "J": (UP, LEFT),
    "7": (DOWN, LEFT),
    "F": (DOWN, RIGHT)
}

def add_points(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return r1+r2, c1+c2

# Determine where to start heading
def where_to_start(start, network):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = start
            pipe = r+dr, c+dc
            if pipe in network and start in network[pipe]:
                return pipe

def start_pipe_type(start, network):
    connects_to_start = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = start
            pipe = r+dr, c+dc
            if pipe in network and start in network[pipe]:
                connects_to_start.append((dr, dc))
    assert len(connects_to_start) == 2
    for key, value in pipes.items():
        if all(d in value for d in connects_to_start):
            return key
    assert False

def length_of_loop(start, network):
    at = where_to_start(start, network)
    prev = start
    length = 1
    while at != start:
        one, two = network[at]
        if one == prev:
            prev, at = at, two
        if two == prev:
            prev, at = at, one
        length += 1
    return length

def get_loop(start, network):
    at = where_to_start(start, network)
    prev = start
    loop = {start, at}
    while at != start:
        one, two = network[at]
        if one == prev:
            prev, at = at, two
        if two == prev:
            prev, at = at, one
        loop.add(at)
    return loop

def nr_enclosed_points(loop, data):
    minr = min(x[0] for x in loop)
    maxr = max(x[0] for x in loop)
    minc = min(x[1] for x in loop)
    maxc = max(x[1] for x in loop)
    inside = []

    # For each point in the "bounding square" of
    # the loop count the number of intersects with
    # the loop to the right.
    # If that number is odd the starting point is
    # enclosed within the loop.
    #
    # Check only JL and | because 
    # each J or L must eventually be followed by 7 or J
    # and the | is always an intersection.
    for r in range(minr, maxr):
        for c in range(minc, maxc):
            start = (r, c)
            intersects = 0
            at = (r, c)
            while at[1] < maxc + 1:
                ir, ic = add_points(at, (-1, -1))
                char = data[ir][ic]
                if at in loop and char in "JL|":
                    intersects += 1
                
                at = add_points(at, RIGHT)

            if intersects != 0 and intersects % 2 == 1 and start not in loop:
                inside.append(start)

    
    return len(inside)

with open(0) as file:
    network = {}
    data = file.read().splitlines()
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char == ".":
                continue
            if char in pipes:
                curr = (r+1, c+1)
                con1, con2 = pipes[char]
                network[curr] = [add_points(curr, con1), add_points(curr, con2)]
            if char in "sS":
                start_r = r
                start = (r+1, c+1)
    
    start_type = start_pipe_type(start, network)
    data[start_r] = data[start_r].replace("S", start_type)

length = length_of_loop(start, network)
distance = length // 2
assert distance == length / 2, "Uneven length?"
print(length // 2)

loop = get_loop(start, network)
# print(loop)
inside = nr_enclosed_points(loop, data)
print(inside)