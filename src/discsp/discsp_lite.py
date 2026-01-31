import json
import argparse
from collections import defaultdict

# Global graph data
NODES = []
EDGES = []
COLORS = []
NEIGHBORS = {}


def load_problem(file_path):
    """Load graph from JSON file (same format as csp)."""
    global NODES, EDGES, COLORS, NEIGHBORS
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    NODES = data["NODES"]
    EDGES = [tuple(e) for e in data["EDGES"]]  
    COLORS = data["COLORS"]

    NEIGHBORS = {n: set() for n in NODES}
    for u, v in EDGES:
        NEIGHBORS[u].add(v)
        NEIGHBORS[v].add(u)


class Agent:
    """DisCSP Agent with local state and message handling."""

    def __init__(self, name, priority):
        self.name = name
        self.priority = priority
        self.value = None
        self.agent_view = {}   # assignments from higher-priority neighbors
        self.inbox = []        # received OK messages
        self.nogoods = []      # stored nogoods (logged only)
        
    def process_messages(self):
        """Process received OK messages and update agent_view."""
        for sender, value in self.inbox:
            self.agent_view[sender] = value
        self.inbox = []

    def is_consistent(self, color):
        """Check if color is consistent with known neighbor assignments."""
        for nbr in NEIGHBORS[self.name]:
            if nbr in self.agent_view and self.agent_view[nbr] == color:
                return False
        return True
    
    def assign_value(self):
        """Try to find a consistent color. Returns True if found, False otherwise."""
        for color in COLORS:
            if self.is_consistent(color):
                self.value = color
                return True
        return False
    
    def get_ok_message(self):
        """Generate OK message to send to lower-priority agents."""
        return (self.name, self.value)


def solve_discsp(graph_file):
    """
    DisCSP-lite: one-pass ordered assignment with OK-message propagation.

    Includes:
    - Per-agent local state
    - OK messages along constraint edges
    - Nogood logging (no backpropagation)

    Does NOT include:
    - Reassignment / backtracking
    - NOGOOD message handling
    - Asynchrony

    Intended as a lightweight bridge from CSP to DCOP/DPOP.
    """

    load_problem(graph_file)
    priority = sorted(NODES)

    agents = {name: Agent(name, i) for i, name in enumerate(priority)}
    message_queue = defaultdict(list)

    for agent_name in priority:
        agent = agents[agent_name]

        # Receive OK messages from higher-priority neighbors
        agent.inbox = message_queue[agent_name]
        agent.process_messages()

        if not agent.assign_value():
            # Log nogood (higher-priority neighbors only)
            nogood = {
                n: agents[n].value
                for n in NEIGHBORS[agent_name]
                if agents[n].priority < agent.priority
            }
            agent.nogoods.append(nogood)
            return None

        # send OK only to lower-priority NEIGHBORS
        ok_msg = agent.get_ok_message()
        for nbr in NEIGHBORS[agent_name]:
            if agents[nbr].priority > agent.priority:
                message_queue[nbr].append(ok_msg)

    return {name: agents[name].value for name in NODES}


def main():
    parser = argparse.ArgumentParser(description="DisCSP-lite Graph Coloring")
    parser.add_argument("graph_file", help="Path to JSON graph file")
    args = parser.parse_args()

    result = solve_discsp(args.graph_file)

    if result:
        print("Solution found:")
        for node in sorted(result.keys()):
            print(f"  {node}: {result[node]}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()