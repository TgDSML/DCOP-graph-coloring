import time

COLORS = [0, 1, 2]
COLOR_NAMES = ["Red", "Green", "Blue"]

def edge_utility(x, y):
    # Returns -1 if same color (conflict), 0 if different
    if x == y:
        return -1
    else:
        return 0 

def main():
    t0 = time.perf_counter()

    #  PHASE 1: PSEUDO-TREE SETUP 
    # Graph: A-B-D-C-A (Cycle)
    # Pseudo-tree: A -> B -> D -> C (Chain) with back-edge C -> A

    #  PHASE 2: UTIL PROPAGATION (Bottom-Up) 

    # 1. NODE C (Leaf): Parent=D, Pseudo-Parent=A
    # UTIL_C(d, a) = max_c [ u(C, D) + u(C, A) ]
    UTIL_C_to_D = {}
    ARG_C = {}

    for d in COLORS:
        for a in COLORS:
            best_val = float("-inf")
            best_c = None
            for c in COLORS:
                val = edge_utility(c, d) + edge_utility(c, a)
                if val > best_val:
                    best_val = val
                    best_c = c
            UTIL_C_to_D[(d, a)] = best_val
            ARG_C[(d, a)] = best_c

    # 2. NODE D: Parent=B, Separator={A} (from child C)
    # UTIL_D(b, a) = max_d [ u(D, B) + UTIL_C(d, a) ]
    UTIL_D_to_B = {}
    ARG_D = {}

    for b in COLORS:
        for a in COLORS:
            best_val = float("-inf")
            best_d = None
            for d in COLORS:
                val = edge_utility(d, b) + UTIL_C_to_D[(d, a)]
                if val > best_val:
                    best_val = val
                    best_d = d
            UTIL_D_to_B[(b, a)] = best_val
            ARG_D[(b, a)] = best_d

    # 3. NODE B: Parent=A
    # UTIL_B(a) = max_b [ u(B, A) + UTIL_D(b, a) ]
    UTIL_B_to_A = {}
    ARG_B = {}

    for a in COLORS:
        best_val = float("-inf")
        best_b = None
        for b in COLORS:
            val = edge_utility(b, a) + UTIL_D_to_B[(b, a)]
            if val > best_val:
                best_val = val
                best_b = b
        UTIL_B_to_A[a] = best_val
        ARG_B[a] = best_b

    #  PHASE 3: VALUE PROPAGATION (Top-Down) 

    # 1. Root A
    best_root_val = float("-inf")
    a_best = None
    for a in COLORS:
        if UTIL_B_to_A[a] > best_root_val:
            best_root_val = UTIL_B_to_A[a]
            a_best = a

    # 2. B (knows A)
    b_best = ARG_B[a_best]

    # 3. D (knows B and A)
    d_best = ARG_D[(b_best, a_best)]

    # 4. C (knows D and A)
    c_best = ARG_C[(d_best, a_best)]

    t1 = time.perf_counter()

    #  OUTPUT 
    print("=== DPOP: Diamond Graph (Cycle A-B-D-C) ===")
    print(f"Number of colors: {len(COLORS)}")
    print(f"Runtime: {(t1 - t0)*1000:.3f} ms\n")

    print(" UTIL TABLES (Cost/Utility passed up) ")
    
    print("UTIL_C->D (msg size 9):")
    # Formatting the table for C->D
    header = "      " + "  ".join(f"A={a}" for a in COLORS)
    print(header)
    for d in COLORS:
        row_vals = [UTIL_C_to_D[(d, a)] for a in COLORS]
        print(f"D={d}  " + str(row_vals))
    print()

    print("UTIL_D->B (msg size 9):")
    # Formatting the table for D->B
    header = "      " + "  ".join(f"A={a}" for a in COLORS)
    print(header)
    for b in COLORS:
        row_vals = [UTIL_D_to_B[(b, a)] for a in COLORS]
        print(f"B={b}  " + str(row_vals))
    print()

    print("UTIL_B->A (msg size 3):")
    print(UTIL_B_to_A)
    print()

    print(" FINAL ASSIGNMENT ")
    print(f"A = {a_best} ({COLOR_NAMES[a_best]})")
    print(f"B = {b_best} ({COLOR_NAMES[b_best]})")
    print(f"D = {d_best} ({COLOR_NAMES[d_best]})")
    print(f"C = {c_best} ({COLOR_NAMES[c_best]})")
    print()

    total_utility = (
        edge_utility(a_best, b_best) + 
        edge_utility(b_best, d_best) + 
        edge_utility(d_best, c_best) + 
        edge_utility(c_best, a_best)
    )
    print(f"Total Utility (0 = optimal, negative = conflicts): {total_utility}")

if __name__ == "__main__":
    main()
