from itertools import pairwise
import re

class Map:
    def __init__(self, group):
        self.group = group

    def apply(self, x):
        for out_start, in_start, r in self.group:
            if in_start <= x < in_start+r:
                return x+out_start-in_start
        return x

    def yield_ranges(self, seed_ranges):
        yield from self.yield_ranges_helper(seed_ranges, 0)

    def yield_ranges_helper(self, seed_ranges, start_i):
        # If some ranges did't get mapped, yield them as they are
        # and we are done.
        if start_i >= len(self.group):
            yield from seed_ranges
            return

        for seed_range in seed_ranges:
            out_start, in_start, r = self.group[start_i]
            r_start, r_stop = seed_range
            before = (r_start, min(r_stop, in_start))
            overlap = (max(in_start, r_start), min(in_start+r, r_stop))
            after = (max(in_start+r, r_start), r_stop)
            # Recursively map the splits from the before-portion
            # if there are elements in before
            if before[1] > before[0]:
                yield from self.yield_ranges_helper([before], start_i+1)
            # If there is overlap that can be mapped
            # map it, and we are done with that portion of the range.
            if overlap[1] > overlap[0]:
                o1, o2 = overlap
                overlap = (o1-in_start+out_start, o2-in_start+out_start)
                yield overlap
            # Recursively map the splits from the after-portion
            # if there are elements in after
            if after[1] > after[0]:
                yield from self.yield_ranges_helper([after], start_i+1)
                

with open("input.txt", "r") as file:
    data = file.read().split("\n\n")
    seeds = [int(x) for x in re.findall(r"\d+", data[0])]
    groups = []
    for line in data[1:]:
        ap = []
        for grp in line.split("\n")[1:]:
            ap.append([int(x) for x in grp.split()])
        groups.append(ap)
    
    maps = [Map(group) for group in groups]

out = []
for seed in seeds:
    for mp in maps:
        seed = mp.apply(seed)
    out.append(seed)

print(f"Part 1: {min(out)}")

seed_ranges = [(start, start+sz) for start, sz in list(pairwise(seeds))[::2]]
out = []
for seed_range in seed_ranges:
    seed_range = [seed_range]
    for mp in maps:
        seed_range = list(mp.yield_ranges(seed_range))
    out.append(seed_range)

mn = float("inf")
for group in out:
    for range_ in group:
        mn = min(mn, range_[0])

print(f"Part 2: {mn}")