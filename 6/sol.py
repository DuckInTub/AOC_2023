
with open("input.txt", "r") as file:
    data = file.read().splitlines()
    times = [int(x) for x in data[0].split(":")[1].split(" ") if x]
    dists = [int(x) for x in data[1].split(":")[1].split(" ") if x]


score = 1
for time, dist in zip(times, dists):
    nr = 0
    for t in range(time):
        rem_time = time - t
        speed = t
        if speed * rem_time > dist:
            nr += 1
    score *= nr

print(score)

time = int("".join(str(x) for x in times))
dist = int("".join(str(x) for x in dists))
print(time, dist)

score = 0
for t in range(time):
    rem_time = time - t
    speed = t
    if speed * rem_time > dist:
        score += 1

print(score)