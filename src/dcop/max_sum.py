import json
import random
random.seed(0)

class GraphColoringInstance:
    def __init__(self, name, nodes, edges, colors):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.colors = colors

def load_instance(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    name = data.get('name', 'Instance')
    nodes = data['NODES']
    edges = data['EDGES']
    colors = data['COLORS']
    edges = [(u, v) for u, v in edges]

    return GraphColoringInstance(name, nodes, edges, colors)

def build_neighbors(nodes, edges):
    neighbors = {n: [] for n in nodes}
    for u , v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    return neighbors

def conflict_cost(c1, c2):
    return 1 if c1 == c2 else 0

def normalize(vec):
    m = min(vec)
    return[x - m for x in vec]

def damp(old, new, alpha):
    return [(1 - alpha) * o + alpha * n for o, n in zip(old, new)]

def max_sum(instance, max_iters=50, damping=0.5, tol=1e-6):

    nodes = instance.nodes
    colors = instance.colors
    k = len(colors)

    neighbors = build_neighbors(nodes, instance.edges)

    messages = {}
    for i in nodes:
        for j in neighbors[i]:
            messages[(i, j)] = normalize([random.random() * 1e-3 for _ in range(k)])

    def factor_message(src, dst):
        out = [0.0] * k
        for c_dst in range(k):
            best = float("inf")
            for c_src in range(k):
                val = conflict_cost(c_src, c_dst) + messages[(src, dst)][c_src]
                if val < best:
                    best = val
            out[c_dst] = best
        return normalize(out)

    for iteration in range(max_iters):

        new_messages = {}
        max_delta = 0

        for i in nodes:
            for j in neighbors[i]:

                incoming = [0.0] * k

                for neighbor in neighbors[i]:
                    if neighbor == j:
                        continue

                    factor_to_i = factor_message(neighbor, i)
                    incoming = [a + b for a, b in zip(incoming, factor_to_i)]

                candidate = normalize(incoming)

                old = messages[(i, j)]
                updated = damp(old, candidate, damping)
                updated = normalize(updated)

                new_messages[(i, j)] = updated

                delta = max(abs(a - b) for a, b in zip(old, updated))
                if delta > max_delta:
                    max_delta = delta

        messages = new_messages

        if max_delta < tol:
            break

    # Decode assignment
    assignment_index = {}
    for i in nodes:
        belief = [0.0] * k
        for neighbor in neighbors[i]:
            factor_to_i = factor_message(neighbor, i)
            belief = [a + b for a, b in zip(belief, factor_to_i)]

        best_color = min(range(k), key=lambda c: belief[c])
        assignment_index[i] = best_color

    assignment = {i: colors[assignment_index[i]] for i in nodes}

    conflicts = 0
    for u, v in instance.edges:
        if assignment_index[u] == assignment_index[v]:
            conflicts += 1

    return {
        "assignment": assignment,
        "conflicts": conflicts,
        "iterations": iteration + 1
    }
