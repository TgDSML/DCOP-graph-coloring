import os
import sys
import matplotlib.pyplot as plt
import networkx as nx

# Import από το αρχείο adopt
from src.dcop.adopt import load_instance, run_adopt

def visualize_solution(instance, assignment, title, output_filename):
    """
    Δημιουργεί και αποθηκεύει μια εικόνα του γράφου με τα χρώματα που επιλέχθηκαν.
    """
    G = nx.Graph()
    G.add_nodes_from(instance.nodes)
    G.add_edges_from(instance.edges)

    # Δημιουργία χρωματικής παλέτας
    unique_colors = sorted(list(set(assignment.values())))
    palette = ['#ff6666', '#66ff66', '#6666ff', '#ffff66', '#ff66ff', '#66ffff', '#ffcc66', '#cccccc']
    
    color_map = {}
    for i, color_name in enumerate(unique_colors):
        color_map[color_name] = palette[i % len(palette)]

    node_colors = [color_map[assignment[n]] for n in G.nodes()]

    plt.figure(figsize=(10, 8))
    
    # Επιλογή layout: Spectral για Grid, Spring για τα υπόλοιπα
    if "grid" in instance.name.lower():
        pos = nx.spectral_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, edgecolors='black')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title(title)
    plt.axis('off')
    
    # Αποθήκευση εικόνας
    plt.savefig(output_filename, format="PNG")
    plt.close()
    print(f"   🖼️  Graph image saved to: {output_filename}")

def run_all_experiments():
    # 1. ΠΡΟΣΘΗΚΗ ΤΩΝ ΝΕΩΝ ΑΡΧΕΙΩΝ ΣΤΗ ΛΙΣΤΑ
    graph_files = [
        "examples/graphs/triangle.json",
        "examples/graphs/diamond.json",
        "examples/graphs/grid5x5.json",   # Νέο
        "examples/graphs/random30.json"   # Νέο
    ]

    # Δημιουργία φακέλου για τα αποτελέσματα
    if not os.path.exists("results"):
        os.makedirs("results")

    print("========================================")
    print("      DCOP ADOPT EXPERIMENTS           ")
    print("========================================\n")

    for file_path in graph_files:
        if not os.path.exists(file_path):
            print(f"❌ Error: File NOT found: {file_path}")
            print("----------------------------------------\n")
            continue

        try:
            # Φόρτωση
            instance = load_instance(file_path)
            
            print(f"🧪 Experiment: {instance.name}")
            print(f"   File: {file_path}")
            print(f"   Nodes: {len(instance.nodes)}, Colors: {len(instance.colors)}")
            
            # 2. ΑΥΞΗΣΗ ITERATIONS (Για να προλαβαίνουν τα μεγάλα graphs)
            limit = 10000 
            result = run_adopt(instance, max_iters=limit)
            
            # Εκτύπωση Αποτελεσμάτων
            print(f"   ✅ Finished in {result['iterations']} iterations.")
            
            if result['conflicts'] == 0:
                print("   🎉 STATUS: SUCCESS (0 Conflicts)")
            else:
                print(f"   ⚠️ STATUS: FAILED ({result['conflicts']} Conflicts)")
                
            # 3. ΑΠΟΚΡΥΨΗ ΜΕΓΑΛΩΝ ΛΙΣΤΩΝ (Για να μην γεμίζει η κονσόλα)
            if len(instance.nodes) <= 10:
                sorted_assignment = dict(sorted(result['assignment'].items()))
                print(f"   Assignment: {sorted_assignment}")
            else:
                print(f"   Assignment: (Hidden for brevity - {len(instance.nodes)} nodes)")
            
            # 4. ΚΛΗΣΗ ΤΗΣ ΟΠΤΙΚΟΠΟΙΗΣΗΣ
            output_img = f"results/{instance.name}_solution.png"
            visualize_solution(instance, result['assignment'], 
                             f"ADOPT: {instance.name} ({result['conflicts']} Conflicts)", 
                             output_img)
            
        except Exception as e:
            print(f"❌ Error during execution: {e}")

        print("----------------------------------------\n")

if __name__ == "__main__":
    run_all_experiments()