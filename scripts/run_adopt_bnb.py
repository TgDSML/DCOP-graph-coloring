import os
import json
import matplotlib.pyplot as plt
import networkx as nx

# Εισάγουμε μόνο τη Λογική από το άλλο αρχείο
from src.dcop.adopt_bnb import solve_adopt_bnb, GraphColoringInstance

def load_instance(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    edges = [tuple(e) for e in data['EDGES']]
    return GraphColoringInstance(data.get('name','Inst'), data['NODES'], edges, data['COLORS'])

def visualize_solution(instance, assignment, title):
    G = nx.Graph()
    G.add_nodes_from(instance.nodes)
    G.add_edges_from(instance.edges)

    unique_colors = sorted(list(set(assignment.values())))
    palette = ['#ff6666', '#66ff66', '#6666ff', '#ffff66', '#ff66ff', '#66ffff']
    color_map = {color: palette[i % len(palette)] for i, color in enumerate(unique_colors)}
    node_colors = [color_map[assignment[n]] for n in G.nodes()]

    plt.figure(figsize=(10, 8))
    # Ειδικό layout για το Grid
    if "grid" in instance.name.lower():
        pos = nx.spectral_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)
        
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, edgecolors='black')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title(title)
    plt.axis('off')
    
    print("   🖼️  Displaying graph... (Close the window to continue to the next one)")
    # ΑΝΤΙ ΓΙΑ SAVEFIG, ΚΑΝΟΥΜΕ SHOW
    plt.show()

def main():
    graph_files = [
        "examples/graphs/triangle.json",
        "examples/graphs/diamond.json",
        "examples/graphs/grid5x5.json",
        "examples/graphs/random30.json"
    ]

    print("========================================")
    print("      DCOP ADOPT-BnB EXPERIMENTS       ")
    print("========================================\n")

    for file_path in graph_files:
        if not os.path.exists(file_path):
            print(f"❌ Error: File NOT found: {file_path}")
            print("----------------------------------------\n")
            continue

        instance = load_instance(file_path)
        print(f"🧪 Experiment: {instance.name} (BnB)")
        print(f"   File: {file_path}")
        print(f"   Nodes: {len(instance.nodes)}, Colors: {len(instance.colors)}")
        
        # Κλήση της καθαρής συνάρτησης επίλυσης
        limit = 2000
        result = solve_adopt_bnb(instance, max_iters=limit)
        
        print(f"   ✅ Finished in {result['iterations']} iterations.")
        
        if result['conflicts'] == 0:
            print(f"   🎉 STATUS: SUCCESS (0 Conflicts)")
        else:
            print(f"   ⚠️ STATUS: FAILED ({result['conflicts']} Conflicts)")
            
        # Απόκρυψη μεγάλων λιστών για να μην γεμίζει η κονσόλα
        if len(instance.nodes) <= 10:
            sorted_assignment = dict(sorted(result['assignment'].items()))
            print(f"   Assignment: {sorted_assignment}")
        else:
            print(f"   Assignment: (Hidden for brevity - {len(instance.nodes)} nodes)")

        # Κλήση της οπτικοποίησης (με 3 ορίσματα πλέον!)
        visualize_solution(instance, result['assignment'], 
                         f"BnB: {instance.name} ({result['conflicts']} Conflicts)")
                         
        print("----------------------------------------\n")

if __name__ == "__main__":
    main()