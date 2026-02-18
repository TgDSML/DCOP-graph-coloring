import json
import random

# --- ΒΟΗΘΗΤΙΚΕΣ ΚΛΑΣΕΙΣ ΚΑΙ ΣΥΝΑΡΤΗΣΕΙΣ ---
class GraphColoringInstance:
    def __init__(self, name, nodes, edges, colors):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.colors = colors

def load_instance(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    edges = [tuple(e) for e in data['EDGES']]
    return GraphColoringInstance(data.get('name','Inst'), data['NODES'], edges, data['COLORS'])

def get_neighbors(node, edges):
    nbrs = []
    for u, v in edges:
        if u == node: nbrs.append(v)
        elif v == node: nbrs.append(u)
    return nbrs

# --- ΚΑΤΑΣΚΕΥΗ PSEUDO-TREE (Recursive DFS) ---
def build_pseudotree(nodes, edges, root):
    parent = {n: None for n in nodes}
    children = {n: [] for n in nodes}
    pseudo_parents = {n: [] for n in nodes} 
    pseudo_children = {n: [] for n in nodes}
    
    visited = set()

    def dfs(u, p):
        visited.add(u)
        
        # Tree Edges
        if p is not None:
            parent[u] = p
            children[p].append(u)
            
        for v in get_neighbors(u, edges):
            if v == p:
                continue 
            
            if v in visited:
                # Back-edges (Πρόγονοι)
                if v not in pseudo_parents[u]:
                    pseudo_parents[u].append(v)
                    pseudo_children[v].append(u) # Σημαντικό για την επικοινωνία
            else:
                dfs(v, u)

    dfs(root, None)
    return parent, children, pseudo_parents, pseudo_children

# --- Η ΚΛΑΣΗ ΤΟΥ ΠΡΑΚΤΟΡΑ ---
class AdoptAgent:
    def __init__(self, agent_id, domain, parent, children, pseudo_parents, pseudo_children):
        self.id = agent_id
        self.domain = domain 
        self.value = random.choice(domain) # Τυχαία αρχή
        
        self.parent = parent
        self.children = children
        self.pseudo_parents = pseudo_parents
        self.pseudo_children = pseudo_children
        
        self.current_context = {} 
        self.costs = {child: 0 for child in children} 
        
    def calculate_local_cost(self, val):
        cost = 0
        # Έλεγχος με Γονιό
        if self.parent and self.parent in self.current_context:
            if self.current_context[self.parent] == val:
                cost += 1
        # Έλεγχος με Ψευδο-γονείς
        for pp in self.pseudo_parents:
            if pp in self.current_context:
                if self.current_context[pp] == val:
                    cost += 1
        return cost

    def choose_best_value(self):
        best_val = self.value
        min_cost = float('inf')
        
        # Shuffle για αποφυγή μεροληψίας
        shuffled_domain = self.domain[:]
        random.shuffle(shuffled_domain)
        
        for d in shuffled_domain:
            local = self.calculate_local_cost(d)
            total = local + sum(self.costs.values())
            
            if total < min_cost:
                min_cost = total
                best_val = d
        
        return best_val, min_cost

# --- Ο ΚΥΡΙΟΣ ΑΛΓΟΡΙΘΜΟΣ ---
def run_adopt(instance, max_iters=100):
    nodes = instance.nodes
    colors = instance.colors
    edges = instance.edges
    
    # 1. Setup
    root = nodes[0]
    parents, children, p_parents, p_children = build_pseudotree(nodes, edges, root)
    
    agents = {}
    for n in nodes:
        agents[n] = AdoptAgent(n, colors, parents[n], children[n], p_parents[n], p_children[n])
        
    messages = [] 
    
    # 2. Main Loop
    for iteration in range(max_iters):
        current_msgs = messages[:]
        messages = [] 
        changes = False
        sorted_nodes = nodes 
        
        for agent_id in sorted_nodes:
            agent = agents[agent_id]
            my_msgs = [m for m in current_msgs if m[1] == agent_id]
            
            # Επεξεργασία
            for sender, _, msg_type, data in my_msgs:
                if msg_type == "VALUE":
                    agent.current_context[sender] = data
                elif msg_type == "COST":
                    agent.costs[sender] = data
            
            # Απόφαση
            old_val = agent.value
            new_val, cost = agent.choose_best_value()
            
            # Inertia (20% πιθανότητα να μην αλλάξει για να σπάσει ο συγχρονισμός)
            if new_val != old_val:
                if random.random() < 0.2: 
                    new_val = old_val
            
            agent.value = new_val
            
            # Αποστολή
            if new_val != old_val or iteration == 0:
                changes = True
                for child in agent.children:
                    messages.append((agent.id, child, "VALUE", new_val))
                for p_child in agent.pseudo_children:
                    messages.append((agent.id, p_child, "VALUE", new_val))
            
            total_cost = agent.calculate_local_cost(agent.value) + sum(agent.costs.values())
            
            if agent.parent:
                messages.append((agent.id, agent.parent, "COST", total_cost))

        if not changes and iteration > 5:
            break
            
    # 3. Συλλογή αποτελεσμάτων
    assignment = {a_id: agents[a_id].value for a_id in agents}
    
    conflicts = 0
    for u, v in edges:
        if assignment[u] == assignment[v]:
            conflicts += 1
            
    return {
        "assignment": assignment,
        "conflicts": conflicts,
        "iterations": iteration + 1
    }