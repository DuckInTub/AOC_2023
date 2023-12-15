from functools import reduce


def roll_row_east(row):
    indices = []
    curr_stones = 0
    new = []
    
    for i, char in enumerate(row):
        if char == "O":
            curr_stones += 1
        if char == "#":
            indices += [i - x - 1 for x in range(curr_stones)]
            curr_stones = 0
    
    indices += [i - x for x in range(curr_stones)]
    new = []
    for i, char in enumerate(row):
        if char == "#":
            new.append("#")
            continue
        if i in indices:
            new.append("O")
            continue
        new.append(".")

    assert len(new) == len(row)
    return new

def transpose(array):
    return [col for col in zip(*array)]

def roll_east(array):
    return [roll_row_east(row) for row in array]

def roll_west(array):
    mirror = [row[::-1] for row in array]
    roll = roll_east(mirror)
    return [row[::-1] for row in roll]

def roll_south(array):
    return transpose(roll_east(transpose(array)))

def roll_north(array):
    return transpose(roll_west(transpose(array)))

def spin_cycle(array):
    arr = roll_north(array)
    arr = roll_west(arr)
    arr = roll_south(arr)
    return roll_east(arr)

def north_strain(array):
    strain = 0
    for i, row in enumerate(reversed(array)):
        nr_O = sum(1 for c in row if c == "O")
        strain += nr_O*(i+1)

    return strain

def uid(array):
    rows = []
    bit_or = lambda x, y : x | y
    for _, row in enumerate(array):
        rows.append(reduce(bit_or, [2 ** i for i, char in enumerate(row) if char == "O"], 0))
    return tuple(rows)


with open(0) as file:
    data = file.read().splitlines()

p1 = north_strain(roll_north(data))
print(f"Part 1: {p1}")

# The spin-cycle will eventually actually cycle
# so for each spin-cycle add that to a list
# then always check if some number of previous cycles match
# if that is the case we can add the length of that cycle to i
# and then continue until we reach the limit of 1_000_000_000

i = 0
limit = 1_000_000_000
seen = {}
last = []
cycled = False
spun = data
back_len = 5
while i < limit:
    i += 1
    spun = spin_cycle(spun)

    if cycled:
        continue

    key = uid(spun)
    last = last[-(back_len-1):]
    last.append(key)
    key = tuple(last)

    if key in seen:
        prevI = seen[key]
        cyc_len = i - prevI
        print(f"CYCLE FOUND OF LEN {cyc_len}, AFTER {i} ITERATIONS!")
        # i + X*cyc_len < limit
        repeat = (limit - i) // cyc_len
        i += cyc_len * repeat
        print(f"NEW i {i}")
        cycled = True

    if len(last) == back_len:
        seen[key] = i

p2 = north_strain(spun)
print(f"Part 2: {p2}")