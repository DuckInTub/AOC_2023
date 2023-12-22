from collections import deque
from multiprocessing import Pool
from time import perf_counter

class Rock:
    def __init__(self, string : str):
        fr, to = string.split("~")
        fr = tuple(int(x) for x in fr.split(","))
        to = tuple(int(x) for x in to.split(","))
        diff = [f != t for f, t in zip(fr, to)]
        d = -1
        if True in diff:
            d = diff.index(True)
        if d == -1:
            self.pos = set([fr])
            self.z = fr[2]
            return
        
        self.pos = set()
        for i in range(to[d] - fr[d] + 1):
            point = list(fr)
            point[d] += i
            self.pos.add(tuple(point))
        self.z = min(p[2] for p in self.pos)
    
    def get_z(self):
        return self.z

    def set_z(self, new_z):
        new_pos = set()
        for p in self.pos:
            p = list(p)
            d = p[2] - self.z
            p[2] = new_z + d
            new_pos.add(tuple(p))
        
        assert len(new_pos) == len(self.pos)
        self.z = new_z
        self.pos = set(new_pos)
    
    def __str__(self):
        return f"{self.pos}"
    
with open(0) as file:
    data = file.read().rstrip().splitlines()
    rocks = [Rock(line) for line in data]
    rocks.sort(key=lambda x : x.get_z())

start = perf_counter()
min_x = min(min(p[0] for p in r.pos) for r in rocks)
min_y = min(min(p[1] for p in r.pos) for r in rocks)

max_x = max(max(p[0] for p in r.pos) for r in rocks)
max_y = max(max(p[1] for p in r.pos) for r in rocks)

stop = set((x, y, 0) for x in range(min_x, max_x+1) for y in range(min_y, max_y+1))
floor_len = len(stop)

for rock in rocks:
    while not any(p in stop for p in rock.pos):
        rock.set_z(rock.get_z() - 1)
    rock.set_z(rock.get_z() + 1)
    stop = stop.union(rock.pos)

assert len(stop) - floor_len == sum(len(rock.pos) for rock in rocks)
print(f"Time = {perf_counter() - start}")

supports  = {i:set() for i in range(len(rocks))}
supported = {i:set() for i in range(len(rocks))}

def i_supports(i):
    rock = rocks[i]
    above = set()
    supports = set()
    for p in rock.pos:
        x, y, z = p
        above.add((x, y, z+1))

    if any(p[2] != rock.get_z() for p in rock.pos):
        max_z = max(above)
        above = {max_z}
    
    for j, other in enumerate(rocks):
        if any(p in above for p in other.pos):
            supports.add(j)
    
    return i, supports

def can_i_be_removed(i):
    if all(len(supported[j]) > 1 for j in supports[i]):
        return True
    return False

with Pool(6) as pool:
    res = pool.map(i_supports, range(len(rocks)))
    for i, supp in res:
        supports[i] = supp
        for j in supp:
            supported[j].add(i)
    
res2 = map(can_i_be_removed, range(len(rocks)))
can_be_removed = set(i for i, t in enumerate(res2) if t)
p1 = len(can_be_removed)



print(f"Part 1: {p1}")

p2 = 0
chain_starters = set(supports.keys()).difference(can_be_removed)
for i in chain_starters:
    supports_others = supports[i]
    score = 0
    removed = set()
    Q = deque(A for A in supports_others if supported[A] == {i})
    while Q:
        other = Q.popleft()
        removed.add(other)
        score += 1
        for above in supports[other]:
            if len(supported[above].difference(removed)) < 1:
                Q.append(above)

    p2 += score

print(f"Part 2: {p2}")