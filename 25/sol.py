from copy import deepcopy
from collections import defaultdict
from random import choice
import re
from typing import Dict, List

def contraction(graph: Dict[str, List[str]], key : str):
    """Mutate the graph by performing a
    node contraction at node key and
    a random one of it's neighbors"""
    conn1 = graph[key]
    key2 = choice(conn1)
    conn2 = graph[key2]
    new_name = "[" + key + ":" + key2 + "]"
    new_edges = [item for item in conn1+conn2 if item not in [key, key2]]

    for k in set(new_edges) - {key, key2}:
        for i, item in enumerate(graph[k]):
            if item == key or item == key2:
                graph[k][i] = new_name

    graph.pop(key)
    graph.pop(key2)
    graph[new_name] = new_edges

def print_graph(graph):
    for key, value in graph.items():
        print(key," : ", " ".join(value))
    print()

GRAPH = defaultdict(list)
with open(0) as file:
    data = file.read().rstrip().splitlines()

# Construct the graph
for line in data:
    first, *rest = line.replace(":", "").split()
    for conn in rest:
        GRAPH[first].append(conn)
        GRAPH[conn].append(first)

# NOTE: What we actually need to find, is the partitions
# formed by the min cut. This can be done with Karger's algorithm.
# Since we know the min cut is 3, the final two nodes need to have
# three edges between them. These edges will contain the min-cut edges.
# But more importantly if we for each contraction of node V, U name the new
# node V:U. The final two nodes will represent witch nodes are in what partition.
# Multiply the length of those two partitions and we have our answer.
while True:
    copy_graph = deepcopy(GRAPH)
    while len(copy_graph.keys()) > 2:
        random_key = choice(list(copy_graph.keys()))
        contraction(copy_graph, random_key)
    if all(x == 3 for x in[len(copy_graph[key]) for key in copy_graph.keys()]):
        break

final_node1, final_node2 = tuple(copy_graph.keys())
partition1 = re.findall(r"\w+", final_node1)
partition2 = re.findall(r"\w+", final_node2)
len_prod = len(partition1) * len(partition2)
print(f"Part 1: {len_prod}")