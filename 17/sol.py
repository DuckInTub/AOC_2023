from heapq import heappop, heappush

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)

DIRS = [UP, RIGHT, DOWN, LEFT]
def turn(fc, d):
    if d == "L":
        return DIRS[(DIRS.index(fc) - 1) % len(DIRS)]
    return DIRS[(DIRS.index(fc) + 1) % len(DIRS)]

def add_points(p1, p2):
    r1, c1 = p1
    r2, c2 = p2
    return r1+r2, c1+c2

def path(array, start, facing):
    seen = set()
    Q = [(0, start, facing, 0)]
    mn = float("inf")
    # States are: heat loss, at, facing, steps since turning
    while Q:
        loss, at, fc, turn_timer = heappop(Q)
        at = add_points(at, fc)
        r, c = at
        # at finish:
        if r == len(array) - 1 and c == len(array[0]) - 1:
            return loss + array[r][c]

        # State seen
        if (at, fc, turn_timer) in seen:
            continue
        seen.add((at, fc, turn_timer))
        # out of bounds:
        if not (0 <= c < len(array[0]) and 0 <= r < len(array)):
            continue
        loss += array[r][c]

        if not turn_timer >= 2:
            heappush(Q, (loss, at, fc, turn_timer + 1))
        heappush(Q, (loss, at, turn(fc, "R"), 0))
        heappush(Q, (loss, at, turn(fc, "L"), 0))
    
def part2_path(array, start, facing):
    seen = set()
    Q = [(0, start, facing, 0)]
    # States are: heat loss, at, facing, steps since turning
    while Q:
        loss, at, fc, turn_timer = heappop(Q)
        at = add_points(at, fc)
        r, c = at
        # at finish:
        if r == len(array) - 1 and c == len(array[0]) - 1 and turn_timer >= 3:
            return loss + array[r][c]

        # State seen
        if (at, fc, turn_timer) in seen:
            continue
        seen.add((at, fc, turn_timer))
        # out of bounds:
        if not (0 <= c < len(array[0]) and 0 <= r < len(array)):
            continue
        loss += array[r][c]

        if turn_timer < 9:
            heappush(Q, (loss, at, fc, turn_timer + 1))
        if turn_timer >= 3:
            heappush(Q, (loss, at, turn(fc, "R"), 0))
            heappush(Q, (loss, at, turn(fc, "L"), 0))
    

with open(0) as file:
    data = file.read().splitlines()
    data = [[int(x) for x in row.strip()] for row in data]

p1 = path(data, (0, 0), RIGHT)
print(f"Part 1: {p1}")
p2 = part2_path(data, (0, 0), RIGHT)
print(f"Part 2: {p2}")
