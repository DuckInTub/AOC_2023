from collections import Counter

def get_hand_type(hand):
    count = Counter(hand)
    # PENTA!
    if not len(count.values()) > 1:
        return 7
    mx_next = tuple(sorted(count.values(), reverse=True)[:2])
    # Junk, Pair, Two pairs, Triple, Full house, Quad, PENTA!
    hand_types = [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1), (5, 0)]
    return hand_types.index(mx_next)

def hand_key(handbid):
    values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"][::-1]
    hand, bid = handbid
    type_ = get_hand_type(hand)
    order = [values.index(card) for card in hand]
    return (type_, order)

with open("input.txt", "r") as file:
    data = [line.split() for line in file.read().splitlines()]

data = list(sorted(data, key=hand_key))
print(list(d[0] for d in data))
score = 0
for i, handbid in enumerate(data):
    score += (i+1)*int(handbid[1])

print(score)