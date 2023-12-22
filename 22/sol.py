from collections import deque
from copy import deepcopy
from multiprocessing import Pool

class Rock:
    def __init__(self, string : str):
        sx, sy, sz, ex, ey, ez = map(int, string.replace("~", ",").split(","))
        self.start = (sx, sy, sz)
        self.end = (ex, ey, ez)

    def get_z(self):
        return self.start[2]

    def set_z(self, new_z):
        sx, sy, sz = self.start
        ex, ey, ez = self.end
        d = ez - sz
        self.start = (sx, sy, new_z)
        self.end = (ex, ey, new_z+d)
        return new_z
    
    def nr(self):
        return 1 + sum(e - s for e, s in zip(self.end, self.start))
    
    def get_points(self):
        points = set()
        for x in range(self.start[0], self.end[0] + 1):
            for y in range(self.start[1], self.end[1] + 1):
                for z in range(self.start[2], self.end[2] + 1):
                    points.add((x, y, z))
        return points
    
    def overlap(self, other):
        return not any([
            other.end[0] < self.start[0],
            other.start[0] > self.end[0],
            other.end[1] < self.start[1],
            other.start[1] > self.end[1],
            other.end[2] < self.start[2],
            other.start[2] > self.end[2],
        ])
    
    def fall(self, stopped, floor : int):
        # Not inside the floor and doesn't intersect stopped blocks
        while self.get_z() != floor and not self.get_points() & stopped:
            self.set_z(self.get_z() - 1)
        self.set_z(self.get_z() + 1)
        return self.get_z()
    
    def __str__(self):
        return f"Start: {self.start}, End: {self.end}"
    
with open(0) as file:
    data = file.read().rstrip().splitlines()
    rocks = [Rock(line) for line in data]
    number_rock_blocks = sum(r.nr() for r in rocks)
    rocks.sort(key=lambda x : x.get_z())

# Make the rocks fall
stopped = set()
for i, rock in enumerate(rocks):
    rock.fall(stopped, 0)
    stopped |= rock.get_points()
assert number_rock_blocks == len(stopped)

def i_supports(i):
    copy_rock = deepcopy(rocks[i])
    copy_rock.set_z(copy_rock.get_z() + 1)
    i_support = set()
    for j, rock in enumerate(rocks):
        if i == j:
            continue
        if copy_rock.overlap(rock):
            i_support.add(j)
    
    return (i, i_support)

def can_i_be_removed(i):
    if all(len(supported[j]) > 1 for j in supports[i]):
        return True
    return False

supports  = {i:set() for i in range(len(rocks))}
supported = {i:set() for i in range(len(rocks))}
with Pool(12) as pool:
    for i, supp in pool.map(i_supports, range(len(rocks))):
        supports[i] = supp
        for j in supp:
            supported[j].add(i)
    
res = [can_i_be_removed(i) for i in supports]
can_be_removed = set(i for i, t in enumerate(res) if t)
fall_starters =  set(i for i, t in enumerate(res) if not t)
p1 = len(can_be_removed)
print(f"Part 1: {p1}")

p2 = 0
for i in fall_starters:
    removed = set()
    Q = deque(A for A in supports[i] if supported[A] == {i})
    while Q:
        at = Q.popleft()
        removed.add(at)
        for above in supports[at]:
            if len(supported[above] - removed) < 1:
                Q.append(above)

    p2 += len(removed)

print(f"Part 2: {p2}")