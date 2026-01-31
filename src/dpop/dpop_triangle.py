# DPOP example: 3-node triangle graph coloring problem

COLORS = [0, 1, 2]

def edge_utility(x, y):
    """Utility for an edge constraint: 0 if colors differ, -1 if same."""
    if x == y:
        return -1
    else:
        return 0
    
# Triangle edges:  (A, B), (B, C), (C, A)
# Pseudotree : A -> B -> C, with back-edge C -> A
# P(C)=B, PP(C) = {A} => UTIL_C_to_B depends on (A, B)

# Phase 2: UTIL propagation
# (a, b) each in {0,1,2}x{0,1,2}
# UTIL_{C -> B}(a, b) = max_c [ u(B, C) + u(A, C) ]

UTIL_C_to_B = {}  # (a, b) -> utility

#Needed later for value propagation
ARG_C = {}        # (a, b) -> best c achieving that utility 

for a in COLORS:
    for b in COLORS:
        # holds the best utility value found so far, '-inf' at start, any real val is better
        best_val = float("-inf")
        # will store the color for C that achieves that best value
        best_c = None
        for c in COLORS:
            val = edge_utility(b,c) + edge_utility(c,a)
            if val > best_val:
                best_val = val
                best_c = c
        UTIL_C_to_B[(a,b)] = best_val
        ARG_C[(a,b)] = best_c

# UTIL_{B -> A}(a) = max_b [ u(A, B) + UTIL_{C -> B}(a, b)
UTIL_B_to_A = {}   # a -> utility
ARG_B = {}         # a -> best b achieving that utility

for  a in COLORS:
    best_val = float("-inf")
    best_b = None
    for b in COLORS:
        val = edge_utility(a,b) + UTIL_C_to_B[(a,b)]
        if val > best_val:
            best_val = val
            best_b = b
    UTIL_B_to_A[a] = best_val
    ARG_B[a] = best_b

# Root A chooses best a
a_best = max(COLORS, key=lambda a: UTIL_B_to_A[a])

# PHASE 3: VALUE propagation
b_best = ARG_B[a_best]

# B -> C: C picks best c given (a_best, b_best) because A  is in C's context
c_best = ARG_C[(a_best, b_best)]

def print_2d_util_table(title, util_dict):
    print(title)
    header = "     " + "  ".join(f"B={b}" for b in COLORS)
    print(header)
    for a in COLORS:
        row = [util_dict[(a, b)] for b in COLORS]
        print(f"A={a} " + "  ".join(f"{v:>3}" for v in row))
    print()

print_2d_util_table("UTIL(C -> B)(A,B):", UTIL_C_to_B)

print("UTIL(B -> A)(A):")
for a in COLORS:
    print(f"  A={a}: {UTIL_B_to_A[a]}   (best B={ARG_B[a]})")
print()

print("Chosen assignment via VALUE propagation:")
print(f"  A = {a_best}")
print(f"  B = {b_best}")
print(f"  C = {c_best}")
print()

total_utility = (
    edge_utility(a_best, b_best) +
    edge_utility(b_best, c_best) +
    edge_utility(c_best, a_best)
)
print(f"Total utility (sum over edges AB, BC, CA) = {total_utility}")
