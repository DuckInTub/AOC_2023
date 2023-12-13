from collections import defaultdict
from functools import cache

def nr(pattern, seq_lens):
    p_len = len(pattern)
    s_len = len(seq_lens)

    # gi : group index witch group are we on in seq_lens
    # li : from what index and forward are we considering in pattern
    @cache
    def inner(gi, li):

        # if there is no more pattern
        if li >= p_len:
            return 1 if gi >= s_len else 0

        # if there is no more sequences
        if gi >= s_len:
           return 0 if "#" in pattern[li:] else 1
        
        n = 0
        # If the first carachter is a ? add
        # the nr of ways if we consider it a .
        if pattern[li] in "?.":
            n += inner(gi, li+1)
        
        # If the first carachter is a ? add
        # the nr of ways after starting a block from here
        if pattern[li] in "?#":
            curr_len = seq_lens[gi]
            # If we can start a valid block here
            # add the nr after starting that block
            enough_len = curr_len <= len(pattern[li:])
            contigous = "." not in pattern[li:li+curr_len]
            exhaust = curr_len == len(pattern[li:])
            try:
                next_ok = pattern[li + curr_len] in ".?"
            except IndexError:
                next_ok = True
            separated = exhaust or next_ok
            if all([enough_len, contigous, separated]):
                n += inner(gi+1, li+curr_len+1)
        
        return n
    
    return inner(0, 0)

with open(0) as file:
    data = file.read().splitlines()
    parsed = []
    for line in data:
        pattern, seq_lens = line.split()
        seq_lens = [int(x) for x in seq_lens.split(",")]
        parsed.append([pattern, seq_lens])
    

p1 = 0
p2 = 0
for pattern, seq_lens in parsed:
    n = nr(pattern, seq_lens)
    # print(pattern, seq_lens)
    p1 += n
    new_pattern = "?".join(5*[pattern])
    n = nr(new_pattern, 5*seq_lens)
    p2 += n

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")