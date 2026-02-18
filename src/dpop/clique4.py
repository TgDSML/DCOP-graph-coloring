

# DPOP on a 4-node clique K4: edges between every pair of {A,B,C,D}
# Pseudotree: A -> B -> C -> D
# Back-edges: C-A, D-A, D-B
#
# Context (separator) sets:
# - D has parent C and pseudo-parents {A,B} => UTIL(D->C) depends on (A,B,C) => size d^3
# - C has parent B and pseudo-parent {A}   => UTIL(C->B) depends on (A,B)   => size d^2
# - B has parent A and no pseudo-parents   => UTIL(B->A) depends on (A)     => size d

import time

COLORS = [0, 1, 2]  # 3 colors
COLOR_NAMES = ["Red", "Green", "Blue"]  # must match len(COLORS)


def edge_utility(x, y):
    """Utility for an edge constraint: 0 if colors differ, -1 if same."""
    return -1 if x == y else 0


def main():
    t0 = time.perf_counter()

    # Phase 2: UTIL propagation

    # UTIL_{D -> C}(a, b, c) = max_d [ u(C,D) + u(A,D) + u(B,D) ]
    UTIL_D_to_C = {}  # (a,b,c) -> utility
    ARG_D = {}        # (a,b,c) -> best d
    for a in COLORS:
        for b in COLORS:
            for c in COLORS:
                best_val = float("-inf")
                best_d = None
                for d in COLORS:
                    val = (
                        edge_utility(c, d) +  # C-D
                        edge_utility(a, d) +  # A-D
                        edge_utility(b, d)    # B-D
                    )
                    if val > best_val:
                        best_val = val
                        best_d = d
                UTIL_D_to_C[(a, b, c)] = best_val
                ARG_D[(a, b, c)] = best_d

    # UTIL_{C -> B}(a, b) = max_c [ u(A,C) + u(B,C) + UTIL_{D -> C}(a,b,c) ]
    UTIL_C_to_B = {}  # (a,b) -> utility
    ARG_C = {}        # (a,b) -> best c
    for a in COLORS:
        for b in COLORS:
            best_val = float("-inf")
            best_c = None
            for c in COLORS:
                val = (
                    edge_utility(a, c) +        # A-C
                    edge_utility(b, c) +        # B-C
                    UTIL_D_to_C[(a, b, c)]      # child contribution
                )
                if val > best_val:
                    best_val = val
                    best_c = c
            UTIL_C_to_B[(a, b)] = best_val
            ARG_C[(a, b)] = best_c

    # UTIL_{B -> A}(a) = max_b [ u(A,B) + UTIL_{C -> B}(a,b) ]
    UTIL_B_to_A = {}  # a -> utility
    ARG_B = {}        # a -> best b
    for a in COLORS:
        best_val = float("-inf")
        best_b = None
        for b in COLORS:
            val = edge_utility(a, b) + UTIL_C_to_B[(a, b)]
            if val > best_val:
                best_val = val
                best_b = b
        UTIL_B_to_A[a] = best_val
        ARG_B[a] = best_b

    # Root A chooses best a
    a_best = max(COLORS, key=lambda a: UTIL_B_to_A[a])

    # Phase 3: VALUE propagation
    b_best = ARG_B[a_best]
    c_best = ARG_C[(a_best, b_best)]
    d_best = ARG_D[(a_best, b_best, c_best)]

    t1 = time.perf_counter()

    # Total utility over all 6 edges in K4: AB, AC, AD, BC, BD, CD
    total_utility = (
        edge_utility(a_best, b_best) +  # A-B
        edge_utility(a_best, c_best) +  # A-C
        edge_utility(a_best, d_best) +  # A-D
        edge_utility(b_best, c_best) +  # B-C
        edge_utility(b_best, d_best) +  # B-D
        edge_utility(c_best, d_best)    # C-D
    )

    # --- 1:1 SUMMARY PRINTS ---
    print("=== DPOP: clique4 (K4) ===")
    print(f"d = {len(COLORS)}")
    print("UTIL table sizes:")
    print(f"  |UTIL(D->C)| = {len(UTIL_D_to_C)} (depends on A,B,C) = d^3")
    print(f"  |UTIL(C->B)| = {len(UTIL_C_to_B)} (depends on A,B)   = d^2")
    print(f"  |UTIL(B->A)| = {len(UTIL_B_to_A)} (depends on A)     = d")
    print(f"Runtime: {(t1 - t0)*1000:.3f} ms\n")

    print("Chosen assignment via VALUE propagation:")
    print(f"  A = {a_best} ({COLOR_NAMES[a_best]})")
    print(f"  B = {b_best} ({COLOR_NAMES[b_best]})")
    print(f"  C = {c_best} ({COLOR_NAMES[c_best]})")
    print(f"  D = {d_best} ({COLOR_NAMES[d_best]})\n")

    print(f"Total utility (sum over all clique edges) = {total_utility}")
    


if __name__ == "__main__":
    main()

