def transpose(array):
    return list(map(list, zip(*array)))

def is_symm_line(line, array):
    up = line-1
    down = line

    for _ in range(len(array)):
        if up < 0 or down >= len(array):
            break
        if array[up] != array[down]:
            return False
        up -= 1
        down += 1
    return True
    
def is_symm_line_with_smudge(line, array):
    up = line-1
    down = line
    smudge = False

    for _ in range(len(array)):
        if up < 0 or down >= len(array):
            break
        for up_char, down_char in zip(array[up], array[down]):
            if up_char != down_char and smudge:
                return False
            elif up_char != down_char:
                smudge = True
        up -= 1
        down += 1
    return smudge

def find_symm_lines(array):
    for i in range(1, len(array)):
        if is_symm_line(i, array):
            return (i, 0)
    
    T = transpose(array)
    for i in range(1, len(T)):
        if is_symm_line(i, T):
            return (0, i)

    return (0, 0)

def find_smudge_line(array):
    for i in range(1, len(array)):
        if is_symm_line_with_smudge(i, array):
            return (i, 0)
    
    T = transpose(array)
    for i in range(1, len(T)):
        if is_symm_line_with_smudge(i, T):
            return (0, i)

    return (0, 0)

with open(0) as file:
    data = file.read()
    if data[-1] == "\n":
        data = data[:-1]
    data = data.split("\n\n")
    data = [group.split("\n") for group in data]

p1 = 0
p2 = 0
for item in data:
    r, c = find_symm_lines(item)
    p1 += 100*r + c
    r, c = find_smudge_line(item)
    p2 += 100*r + c

print(f"Part 1: {p1}")
print(f"Part 2: {p2}")