from copy import deepcopy

def generate_rows(history):
    hist = deepcopy(history)
    rows = [hist]
    row = hist
    while not all(x == 0 for x in rows[-1]):
        new_row = []
        for i in range(len(row) - 1):
            first, second = row[i], row[i+1]
            diff = second - first
            new_row.append(diff)
        rows.append(new_row)
        row = new_row

    return rows

def find_nexts(history):
    rows = generate_rows(history)

    for i, row in list(enumerate(rows[1:]))[::-1]:
        last = row[-1]
        over = rows[i][-1]
        rows[i].append(last + over)

    return rows[0][-1]

def find_prevs(history):
    rows = generate_rows(history)

    for i, row in list(enumerate(rows[1:]))[::-1]:
        first = row[0]
        over = rows[i][0]
        # over - x = first
        # x = over - first
        rows[i].insert(0, over - first)

    return rows[0][0]

with open("input.txt", "r") as file:
    data = [[int(x) for x in line.split()] for line in file.read().splitlines()]
    old_data = deepcopy(data)


print(sum(find_nexts(history) for history in data))
print(sum(find_prevs(history) for history in data))

assert old_data == data, "Some function is mutating by reference"