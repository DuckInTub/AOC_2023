from enum import Enum
from math import lcm
import re
from collections import defaultdict, deque

class Signal(Enum):
    LOW = 0
    HIGH = 1

class State(Enum):
    OFF = 0
    ON = 1

def process(state, memory, rx_feeder):
    Q = deque([("broadcaster", "", Signal.LOW)])
    low = high = 0
    states = dict(state)
    memory = dict(memory)
    rx_feeds = False

    while Q:
        at, frm, signal = Q.popleft()
        type_ = TYPES.get(at, "")

        low  += signal == Signal.LOW
        high += signal == Signal.HIGH

        if type_ == "":
            continue

        if type_ == "b":
            Q += [(conn, at, signal) for conn in CONNECTIONS[at]]
        
        if type_ == "&":
            memory[at][frm] = signal
            send = Signal.HIGH
            if all(v == Signal.HIGH for v in memory[at].values()):
                send = Signal.LOW
            if at == rx_feeder and any(v == Signal.HIGH for v in memory[at].values()):
                rx_feeds = dict(memory[at])
            Q += [(conn, at, send) for conn in CONNECTIONS[at]]
        
        if type_ == "%" and signal == Signal.LOW:
            new_state = [State.ON, State.OFF][states[at].value]
            send_signal = [Signal.HIGH, Signal.LOW][states[at].value]
            states[at] = new_state
            Q += [(conn, at, send_signal) for conn in CONNECTIONS[at]]

    return (low, high), (states, memory), rx_feeds

CONNECTIONS = {}
TYPES = {}
MEMORY = defaultdict(dict)
with open(0) as file:
    data = file.read().rstrip().splitlines()
    for line in data:
        names = re.findall(r"\w+", line)
        name = names[0]
        CONNECTIONS[name] = tuple(names[1:])
        TYPES[name] = line[0]

for name, conns in CONNECTIONS.items():
    for conn in conns:
        if TYPES.get(conn, "") == "&":
            MEMORY[conn][name] = Signal.LOW

(to_rx,) = [key for key in CONNECTIONS if "rx" in CONNECTIONS[key]]
rx_conn_cycle = {key:False for key in MEMORY[to_rx].keys()}

nr_low = 0
nr_high = 0
limit = 1000
state = {key:State.OFF for key in TYPES.keys()}
memory = dict(MEMORY)

for i in range(10 ** 4):
    (low, high), (state, memory), rx_feeds = process(state, memory, to_rx)

    nr_low += low
    nr_high += high

    if i == limit - 1:
        p1 = nr_high * nr_low

    if all(rx_conn_cycle.values()):
        break

    if not rx_feeds:
        continue

    for key, value in rx_feeds.items():
        if value == Signal.HIGH:
            rx_conn_cycle[key] = i+1

print(f"Part 1: {p1}")

for key, value in rx_conn_cycle.items():
    print(f"Cycle found: {key}, {value}")
p2 = lcm(*rx_conn_cycle.values())
print(f"Part 2: {p2}")