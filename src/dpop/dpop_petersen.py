import time
from itertools import product
import matplotlib.pyplot as plt
import networkx as nx

#   #PHASE 1: PSEUDO-TREE SETUP
COLORS = [0, 1, 2]
COLOR_NAMES = ["Red", "Green", "Blue"]
NODES = list(range(10))
# Petersen Graph Edges
EDGES = [
    (0,1), (1,2), (2,3), (3,4), (4,0),  # Outer
    (0,5), (1,6), (2,7), (3,8), (4,9),  # Spokes
    (5,8), (8,6), (6,9), (9,7), (7,5)   # Inner
]

def edge_utility(val1, val2):
    return -1 if val1 == val2 else 0

def print_util_table(node_id, separator, util_table):
    dims = len(separator)
    if dims == 0:
        print(f"UTIL_{node_id}->ROOT: {util_table[()]}")
        return
    parent = separator[0]
    pps = separator[1:]
    
    print(f"UTIL_{node_id}->{parent} (msg size {len(util_table)}):")
    if dims == 1:
        row = [util_table[(p,)] for p in COLORS]
        print(f"  Parent {parent}: {row}")
    elif dims == 2:
        pp1 = pps[0]
        header = "      " + "  ".join(f"PP{pp1}={c}" for c in COLORS)
        print(header)
        for p_val in COLORS:
            row_vals = [util_table[(p_val, pp_val)] for pp_val in COLORS]
            print(f"  P{parent}={p_val}  {row_vals}")
    else:
        print(f"  (Complex {dims}D table, printing raw entries)")
        count = 0
        for k, v in util_table.items():
            print(f"  Ctx{k}: {v}")
            count += 1
            if count > 5: 
                print("  ... (truncated)")
                break
    print()

def dpop():
    t0 = time.perf_counter()
    parent = {0: None}
    children = {i: [] for i in NODES}
    visited = []
    
    stack = [0]
    while stack:
        u = stack[-1]
        if u not in visited:
            visited.append(u)
            neighbors = []
            for e in EDGES:
                if e[0]==u: neighbors.append(e[1])
                elif e[1]==u: neighbors.append(e[0])
            neighbors.sort() 
            
            found = False
            for v in neighbors:
                if v not in visited:
                    parent[v] = u
                    children[u].append(v)
                    stack.append(v)
                    found = True
                    break
            if not found:
                stack.pop()
        else:
            stack.pop()

    # Calculate PPs 
    pp = {i: set() for i in NODES}
    for u in NODES:
        neighbors = []
        for e in EDGES:
            if e[0]==u: neighbors.append(e[1])
            elif e[1]==u: neighbors.append(e[0])
        for v in neighbors:
            if v == parent[u] or v in children[u]: continue
            if visited.index(v) < visited.index(u):
                pp[u].add(v)

    # --- 2. INDUCED SEPARATORS ---
    separator_map = {}
    bottom_up_order = visited[::-1]
    
    for u in bottom_up_order:
        if u == 0: continue
        sep = set()
        sep.add(parent[u])
        sep.update(pp[u])
        
        for c in children[u]:
            child_sep = separator_map[c]
            sep.update(child_sep)
        
        if u in sep: sep.remove(u) 
        separator_map[u] = sorted(list(sep))

    # PHASE 2: UTIL PROPAGATION (Bottom-Up) 
    UTIL = {}
    ARG = {}
    
    print(f"=== DPOP: Petersen Graph (3-Coloring) ===")
    
    print("\n--- Pseudo-tree Structure ---")
    print(f"Root: 0")
    for u in NODES:
        if u == 0: continue
        p = parent[u]
        pps = sorted(list(pp[u]))
        print(f"Node {u}: Parent={p}, PPs={pps}")

    print("\n--- UTIL TABLES (Cost/Utility passed up) ---\n")

    for u in bottom_up_order:
        if u == 0: continue
        
        sep = separator_map[u]
        sep_dims = len(sep)
        
        util_table = {}
        arg_table = {}
        
        for sep_values in product(COLORS, repeat=sep_dims):
            context = dict(zip(sep, sep_values))
            
            best_val = -1
            max_util = float('-inf')
            
            for val_u in COLORS:
                current_util = 0
                for anc in context:
                    if (u, anc) in EDGES or (anc, u) in EDGES:
                        current_util += edge_utility(val_u, context[anc])
                        
                for c in children[u]:
                    child_sep = separator_map[c]
                    child_key = []
                    valid_child = True
                    for var in child_sep:
                        if var == u:
                            child_key.append(val_u)
                        elif var in context:
                            child_key.append(context[var])
                        else:
                            valid_child = False
                            break
                    
                    if valid_child:
                        current_util += UTIL[c][tuple(child_key)]
                
                if current_util > max_util:
                    max_util = current_util
                    best_val = val_u
            
            util_table[tuple(sep_values)] = max_util
            arg_table[tuple(sep_values)] = best_val
            
        UTIL[u] = util_table
        ARG[u] = arg_table
        
        print_util_table(u, sep, util_table)

    # PHASE 3: VALUE PROPAGATION (Top-Down) 
    VALUE = {}
    for u in visited: 
        if u == 0:
            VALUE[u] = 0 
        else:
            sep = separator_map[u]
            key = tuple(VALUE[v] for v in sep)
            VALUE[u] = ARG[u][key]

    t1 = time.perf_counter()
    print(f"Runtime: {(t1 - t0)*1000:.3f} ms\n")

    print("--- FINAL ASSIGNMENT ---")
    sorted_u = sorted(VALUE.keys())
    for u in sorted_u:
        print(f"Node {u}: {COLOR_NAMES[VALUE[u]]}")
    
    conflicts = 0
    for u, v in EDGES:
        if VALUE[u] == VALUE[v]:
            conflicts += 1
    print(f"\nTotal Conflicts: {conflicts}")
    
    # --- VISUALIZATION 1: COLORED GRAPH ---
    G = nx.Graph()
    G.add_edges_from(EDGES)
    
    import math
    pos = {}
    for i in range(5):
        angle = 2 * math.pi * i / 5 - math.pi / 2 
        pos[i] = (math.cos(angle), math.sin(angle))
    for i in range(5):
        node = i + 5
        angle = 2 * math.pi * i / 5 - math.pi / 2
        pos[node] = (0.5 * math.cos(angle), 0.5 * math.sin(angle))
        
    color_map = []
    viz_colors = {0: '#ff6666', 1: '#66ff66', 2: '#6666ff'}
    for node in G.nodes():
        color_map.append(viz_colors[VALUE[node]])
        
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=800, 
            font_color='black', font_weight='bold', edge_color='black', width=1.5)
    plt.title("Petersen Graph 3-Coloring (DPOP Solution)", fontsize=16)
    plt.show()
    plt.close() # Close to start new figure

    # --- VISUALIZATION 2: PSEUDO-TREE ---
    T = nx.DiGraph()
    tree_edges = []
    for u in NODES:
        if parent[u] is not None:
            T.add_edge(parent[u], u)
            tree_edges.append((parent[u], u))
    
    back_edges = []
    for u in NODES:
        for v in pp[u]:
            T.add_edge(u, v)
            back_edges.append((u, v))
    try:
        from networkx.drawing.nx_agraph import graphviz_layout
        pos_tree = graphviz_layout(T, prog='dot')
    except ImportError:
        # Custom shell layout: Root at top, levels below
        levels = {}
        def get_depth(node):
            d = 0
            curr = node
            while parent[curr] is not None:
                curr = parent[curr]
                d += 1
            return d
        
        for n in NODES:
            d = get_depth(n)
            if d not in levels: levels[d] = []
            levels[d].append(n)
        
        pos_tree = {}
        max_depth = max(levels.keys())
        width = max(len(l) for l in levels.values())
        
        for d, nodes in levels.items():
            y = 1.0 - (d / (max_depth + 1))
            chunk = 1.0 / (len(nodes) + 1)
            for i, node in enumerate(nodes):
                x = (i + 1) * chunk
                pos_tree[node] = (x, y)

    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(T, pos_tree, node_color='lightgray', node_size=700, edgecolors='black')
    nx.draw_networkx_labels(T, pos_tree)
    nx.draw_networkx_edges(T, pos_tree, edgelist=tree_edges, edge_color='black', arrows=True, width=2, arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edges(T, pos_tree, edgelist=back_edges, edge_color='red', style='dashed', 
                           connectionstyle='arc3,rad=0.3', arrows=True, width=1.5, arrowstyle='->', arrowsize=15)
    
    import matplotlib.patches as mpatches
    black_patch = mpatches.Patch(color='black', label='Tree Edge (Parent->Child)')
    red_patch = mpatches.Patch(color='red', label='Back Edge (Descendant->Ancestor)')
    plt.legend(handles=[black_patch, red_patch], loc='lower right')
    
    plt.title("DPOP Pseudo-Tree Structure", fontsize=16)
    plt.axis('off')
    plt.show()
    plt.close()

if __name__ == "__main__":
    dpop()
