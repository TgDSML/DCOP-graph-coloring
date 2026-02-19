import random

# --- ΒΟΗΘΗΤΙΚΕΣ ΚΛΑΣΕΙΣ ---
class GraphColoringInstance:
    def __init__(self, name, nodes, edges, colors):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.colors = colors

def get_neighbors(node, edges):
    nbrs = []
    for u, v in edges:
        if u == node: nbrs.append(v)
        elif v == node: nbrs.append(u)
    return nbrs

def build_pseudotree(nodes, edges, root):
    parent = {n: None for n in nodes}
    children = {n: [] for n in nodes}
    pseudo_parents = {n: [] for n in nodes} 
    pseudo_children = {n: [] for n in nodes}
    
    visited = set()
    stack = set()

    def dfs(u, p):
        visited.add(u)
        stack.add(u)
        if p is not None:
            parent[u] = p
            children[p].append(u)
            
        for v in get_neighbors(u, edges):
            if v == p: continue 
            if v in visited:
                if v in stack: # Back-edge
                    if v not in pseudo_parents[u]:
                        pseudo_parents[u].append(v)
                        pseudo_children[v].append(u)
            else:
                dfs(v, u)
        stack.remove(u)

    dfs(root, None)
    return parent, children, pseudo_parents, pseudo_children


# --- ΠΡΑΚΤΟΡΑΣ BnB (ΔΙΟΡΘΩΜΕΝΟΣ) ---
class AdoptBnBAgent:
    def __init__(self, agent_id, domain, parent, children, pseudo_parents, pseudo_children):
        self.id = agent_id
        self.domain = domain 
        self.value = random.choice(domain)
        self.parent = parent
        self.children = children
        self.pseudo_parents = pseudo_parents
        self.pseudo_children = pseudo_children
        
        self.current_context = {} 
        self.child_costs = {child: {val: 0 for val in domain} for child in children} 
        self.bounds = {}

    def calculate_local_cost(self, val):
        cost = 0
        if self.parent and self.parent in self.current_context:
            if self.current_context[self.parent] == val: cost += 1
        for pp in self.pseudo_parents:
            if pp in self.current_context:
                if self.current_context[pp] == val: cost += 1
        return cost

    def get_context_key(self):
        return tuple(sorted(self.current_context.items()))

    def choose_best_value(self):
        context_key = self.get_context_key()
        current_ub = self.bounds.get(context_key, float('inf'))
        
        lbs = {}
        for d in self.domain:
            local = self.calculate_local_cost(d)
            children_cost = sum(self.child_costs[child].get(d, 0) for child in self.children)
            lbs[d] = local + children_cost

        # 1. Βρίσκουμε το ρεαλιστικό ελάχιστο κόστος ΤΩΡΑ
        min_lb = min(lbs.values())

        # 2. Η Διόρθωση (Χαλάρωση του Bound): 
        # Αν η πραγματικότητα (min_lb) είναι χειρότερη από το ρεκόρ μας (UB),
        # σημαίνει ότι το ρεκόρ είναι αδύνατο. Πρέπει να το ανεβάσουμε (Backtrack).
        if min_lb > current_ub:
            self.bounds[context_key] = min_lb
            current_ub = min_lb
        # Αν βρήκαμε νέο καλύτερο, το αποθηκεύουμε
        elif min_lb < current_ub:
            self.bounds[context_key] = min_lb
            current_ub = min_lb

        # 3. Το Pruning: Κρατάμε ΜΟΝΟ όσα χρώματα είναι <= current_ub
        valid_colors = [d for d in self.domain if lbs[d] <= current_ub]
        
        # 4. Διαλέγουμε το καλύτερο
        best_colors = [d for d in valid_colors if lbs[d] == min_lb]
        
        if self.value in best_colors:
            best_val = self.value
        else:
            best_val = random.choice(best_colors)
            
        return best_val, min_lb


# --- Η ΣΥΝΑΡΤΗΣΗ ΕΠΙΛΥΣΗΣ (SOLVER) ---
def solve_adopt_bnb(instance, max_iters=2000):
    nodes = instance.nodes
    edges = instance.edges
    
    root = nodes[0]
    parents, children, p_parents, p_children = build_pseudotree(nodes, edges, root)
    
    agents = {n: AdoptBnBAgent(n, instance.colors, parents[n], children[n], p_parents[n], p_children[n]) for n in nodes}
    messages = [] 
    
    for iteration in range(max_iters):
        current_msgs = messages[:]
        messages = [] 
        
        for agent_id in nodes:
            agent = agents[agent_id]
            incoming = [m for m in current_msgs if m[1] == agent_id]
            for sender, _, msg_type, data in incoming:
                if msg_type == "VALUE":
                    agent.current_context[sender] = data
                elif msg_type == "COST":
                    parent_color, cost_val = data
                    agent.child_costs[sender][parent_color] = cost_val
        
        changes = 0
        for agent_id in nodes:
            agent = agents[agent_id]
            old_val = agent.value
            new_val, min_lb = agent.choose_best_value()
            
            if new_val != old_val:
                if random.random() < 0.1: new_val = old_val
                else: changes += 1
            
            agent.value = new_val
            
            if new_val != old_val or iteration == 0:
                for child in agent.children:
                    messages.append((agent.id, child, "VALUE", new_val))
                for p_child in agent.pseudo_children:
                    messages.append((agent.id, p_child, "VALUE", new_val))
            
            if agent.parent:
                parent_color = agent.current_context.get(agent.parent)
                if parent_color: 
                    # Αλλαγή: Στέλνουμε το ΠΡΑΓΜΑΤΙΚΟ min_lb που βρήκαμε
                    messages.append((agent.id, agent.parent, "COST", (parent_color, min_lb)))
                
    assignment = {a_id: agents[a_id].value for a_id in agents}
    conflicts = 0
    for u, v in edges:
        if assignment[u] == assignment[v]:
            conflicts += 1
            
    return {
        "assignment": assignment,
        "conflicts": conflicts,
        "iterations": max_iters
    }