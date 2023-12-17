from functools import reduce
from time import perf_counter
from timeit import timeit
import multiprocessing as mp

def roll_row_east(row):
    stone_nrs = [sum(1 for ch in group if ch == "O") for group in "".join(row).split("#")]

    curr_stone_group = 0
    new_row = [ch if ch != "O" else "." for ch in row] + ["#"]
    for i, ch in enumerate(new_row):
        if ch == "#":
            for x in range(stone_nrs[curr_stone_group]):
                new_row[i-x-1] = "O"
            curr_stone_group += 1
    
    new_row = new_row[:-1]
    assert len(new_row) == len(row)
    return "".join(new_row)

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
    for row in array:
        rows.append(
        reduce(bit_or, [
            2 ** i 
            for i, char in enumerate(row)
            if char == "O"
        ], 0))
    return tuple(rows)

def strain_uid(uid : tuple[int]):
    strain = 0
    for i, bits in enumerate(reversed(uid)):
        nr_O = bits.bit_count()
        strain += nr_O*(i+1)
    return strain

#               "0123456789"
# print(roll_row_east(".O.#.OO..."))

with open(0) as file:
    data = file.read().splitlines()

p1 = north_strain(roll_north(data))
print(f"Part 1: {p1}")

# The spin-cycle will eventually "cycle" (dumb names)
# so for each spin-cycle add the state to a dict,
# then always check if it matches a previous state.
# If that is the case: we can add the length of that cycle to i,
# until we are just under 1_000_000_000, and then continue normally.
# NOTE: The spin-cycle is completly deterministic of the grid state,
# hence if we ever se the same grid state again,
# we now we can repeat cyclically. The uid() function gives
# us a unique tuple for a given state, so we can check for states.

i = 0
limit = 1_000_000_000
seen = {}
cycled = False
spun = data
while i < limit:
    i += 1
    spun = spin_cycle(spun)

    key = uid(spun)
    if key in seen:
        prevI = seen[key]
        cyc_len = i - prevI
        print(f"CYCLE FOUND OF LEN {cyc_len}, AFTER {i} ITERATIONS!")
        rev_seen = {value:key for key, value in seen.items()}
        eq_final_i = (limit - prevI) % cyc_len + prevI
        print(f"EQUIVALENT INDEX {eq_final_i}")
        final_uid = rev_seen[eq_final_i]
        p2 = strain_uid(final_uid)
        break

    seen[key] = i

print(f"Part 2: {p2}")
