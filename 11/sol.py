from itertools import combinations

def transpose(array):
    return [col for col in zip(*array)]

def manhattan_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

class Universe:
    def __init__(self, galaxies, empt_rows, empt_cols):
        self.galaxies = galaxies
        self.empt_rows = empt_rows
        self.empt_cols = empt_cols
    
    def galaxy_dist(self, p1, p2, expansion_factor):
        r1, c1 = p1
        r2, c2 = p2
        vert_range = range(min(r1, r2)+1, max(r1, r2))
        hor_range = range(min(c1, c2)+1, max(c1, c2))

        vert = 0
        horz = 0
        for r in self.empt_rows:
            if r in vert_range:
                vert += 1
            
        for c in self.empt_cols:
            if c in hor_range:
                horz += 1

        # expansion_factor - 1, because the one empty row and col was already there
        # and thus counted in the manhattan_dist() call.
        dist = manhattan_dist(p1, p2) + (expansion_factor - 1) * (vert + horz)
        return dist


EMPTY_ROWS = []
EMPTY_COLS = []
with open(0) as file:
    data = file.readlines()
    points = set()
    for r, row in enumerate(data):
        if "#" not in row:
            EMPTY_ROWS.append(r+1)
        for c, char in enumerate(row):
            if char == "#":
                points.add((r+1, c+1))
    
    T_data = transpose(data)
    for c, col in enumerate(T_data):
        if "#" not in col:
            EMPTY_COLS.append(c+1)

universe = Universe(points, EMPTY_ROWS, EMPTY_COLS)

score1 = 0
score2 = 0
for p1, p2 in combinations(universe.galaxies, 2):
    score1 += universe.galaxy_dist(p1, p2, 2)
    score2 += universe.galaxy_dist(p1, p2, int(1E6))

print(f"Part 1: {score1}")
print(f"Part 2: {score2}")