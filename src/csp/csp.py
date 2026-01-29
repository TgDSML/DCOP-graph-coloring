import json
import argparse
from pathlib import Path

# Global variables to store graph data
NODES = []
EDGES = []
COLORS = []

def load_graph(file_path):
    """Load graph from a JSON file."""
    global NODES, EDGES, COLORS
    with open(file_path, 'r') as f:
        data = json.load(f)
    NODES = data['NODES']
    EDGES = data['EDGES']
    COLORS = data['COLORS']

def neighbors(node):
    """Return neighbor nodes of 'node' based on undirected edges."""
    nbrs = set()
    for u,v in EDGES:
        if u == node:
            nbrs.add(v)
        elif v == node:
            nbrs.add(u)
    return nbrs

def is_consistent(node, color, assignment):
    """Check if assigning 'color' to 'node' violates any edge constraints."""
    for nbr in neighbors(node):
        if nbr in assignment and assignment[nbr] == color:
            return False
    return True

def select_unassigned_variable(assignment):
    """Pick the next unassigned node(simple order)."""
    for n in NODES:
        if n not in assignment:
            return n


def backtrack(assignment):
    """Backtracking search for a valid coloring."""
    if len(assignment) == len(NODES):
        return assignment # complete solution
    
    node = select_unassigned_variable(assignment)

    for color in COLORS:
        if is_consistent(node, color, assignment):
            assignment[node] = color
            result = backtrack(assignment)
            if result is not None:
                return result
            del assignment[node] # backtrack

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graph Coloring CSP Solver")
    parser.add_argument("graph_file", help="Path to the graph JSON file (e.g., examples/graphs/triangle.json)")
    args = parser.parse_args()
    
    # Load the graph from JSON file
    load_graph(args.graph_file)
    
    solution = backtrack({})
    if solution is None:
        print("No solution found.")
    else:
        print("Solution found:")
        for n in NODES:
            print(f"Node {n}: Color {solution[n]}")    