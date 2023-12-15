def hash(seq : str):
    value = 0
    for char in seq:
        value += ord(char)
        value *= 17
        value %= 256
    
    return value

with open(0) as file:
    data = file.read().rstrip().split(",")

p1 = sum(hash(seq) for seq in data)
print(f"Part 1: {p1}")

BOX = [[] for _ in range(256)]
for seq in data:
    if seq[-1] == "-":
        label = seq[:-1]
        boxnr = hash(label)
        present_labels = [l for l, v in BOX[boxnr]]
        if label in present_labels:
            index = present_labels.index(label)
            BOX[boxnr].pop(index)
    
    elif seq[-2] == "=":
        value = int(seq[-1])
        label = seq[:-2]
        boxnr = hash(label)
        present_labels = [l for l, v in BOX[boxnr]]
        if label in present_labels:
            index = present_labels.index(label)
            BOX[boxnr][index][1] = value
        else:
            BOX[boxnr].append([label, value])
            
p2 = 0
for boxnr, B in enumerate(BOX):
    for i, (label, value) in enumerate(B):
        p2 += (1 + boxnr) * (i + 1) * (value)

print(f"Part 2: {p2}")