import random
import math
from src.dcop.max_sum import build_neighbors, load_instance

def compute_conflicts(edges, assignment_index):
    conflicts = 0
    for u, v in edges:
        if assignment_index[u] == assignment_index[v]:
            conflicts += 1
    return conflicts

def local_cost(node, color_idx, neighbors, assignment_index):
    cost = 0
    for nb in neighbors[node]:
        if assignment_index[nb] == color_idx:
            cost += 1
    return cost


def sample_from_probs(probs):
    r = random.random()
    s = 0
    for i, p in enumerate(probs):
        s += p
        if r <= s:
            return i 
    return len(probs) - 1
    
def dcop_gibbs(instance, max_iters=50, beta=2, seed=10, schedule="random"):
    random.seed(seed)

    nodes = instance.nodes
    edges = instance.edges
    colors = instance.colors
    k = len(colors)

    neighbors = build_neighbors(nodes, edges)

    assignment_index = {n: random.randrange(k) for n in nodes}
    best_assignment_index = dict(assignment_index)
    best_conflicts = compute_conflicts(edges, assignment_index)
    history_best = [best_conflicts]
    iters_to_zero = None

    for t in range(max_iters):

        if schedule == "round_robin":
            node = nodes[t % len(nodes)]
        else:
            node = random.choice(nodes)

        costs = [local_cost(node, c, neighbors, assignment_index) for c in range(k)]
        weights = [math.exp(-beta * cost) for cost in costs]
        Z = sum(weights)
        probs = [w / Z for w in weights] if Z > 0 else [1 / k] * k

        new_color = sample_from_probs(probs)
        assignment_index[node] = new_color

        curr_conflicts = compute_conflicts(edges, assignment_index)
        if curr_conflicts < best_conflicts:
            best_conflicts = curr_conflicts
            best_assignment_index = dict(assignment_index)

        history_best.append(best_conflicts)
        
        if best_conflicts == 0 and iters_to_zero is None:
            iters_to_zero = t + 1
            break

    assignment = {n: colors[best_assignment_index[n]] for n in nodes}
    
    return {
        "assignment": assignment,
        "conflicts": best_conflicts,
        "iterations": t + 1,
        "beta": beta,
        "schedule": schedule,
        "seed": seed,
        "iters_to_zero": iters_to_zero,
        "history_best": history_best
        }













   

