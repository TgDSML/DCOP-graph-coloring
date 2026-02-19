# chain5.py
# DPOP example: 5-node chain graph coloring problem (A-B-C-D-E)
# Pseudotree: A -> B -> C -> D -> E
# Back-edges: none
#
# Separator sizes:
# - E has parent D, no pseudo-parents => UTIL(E->D) depends on (D) => size d
# - D -> C depends on (C) => size d
# - C -> B depends on (B) => size d
# - B -> A depends on (A) => size d

import time

COLORS = [0, 1, 2]  # domain size d
COLOR_NAMES = ["Red", "Green", "Blue"]  # must match len(COLORS)


def edge_utility(x, y):
    """Utility for an edge constraint: 0 if colors differ, -1 if same."""
    return -1 if x == y else 0


def main():
    t0 = time.perf_counter()

    # Phase 2: UTIL propagation

    # UTIL_{E -> D}(d) = max_e [ u(D,E) ]
    UTIL_E_to_D = {}  # d -> utility
    ARG_E = {}        # d -> best e
    for d in COLORS:
        best_val = float("-inf")
        best_e = None
        for e in COLORS:
            val = edge_utility(d, e)  # D-E
            if val > best_val:
                best_val = val
                best_e = e
        UTIL_E_to_D[d] = best_val
        ARG_E[d] = best_e

    # UTIL_{D -> C}(c) = max_d [ u(C,D) + UTIL_{E -> D}(d) ]
    UTIL_D_to_C = {}  # c -> utility
    ARG_D = {}        # c -> best d
    for c in COLORS:
        best_val = float("-inf")
        best_d = None
        for d in COLORS:
            val = edge_utility(c, d) + UTIL_E_to_D[d]  # C-D + child
            if val > best_val:
                best_val = val
                best_d = d
        UTIL_D_to_C[c] = best_val
        ARG_D[c] = best_d

    # UTIL_{C -> B}(b) = max_c [ u(B,C) + UTIL_{D -> C}(c) ]
    UTIL_C_to_B = {}  # b -> utility
    ARG_C = {}        # b -> best c
    for b in COLORS:
        best_val = float("-inf")
        best_c = None
        for c in COLORS:
            val = edge_utility(b, c) + UTIL_D_to_C[c]  # B-C + child
            if val > best_val:
                best_val = val
                best_c = c
        UTIL_C_to_B[b] = best_val
        ARG_C[b] = best_c

    # UTIL_{B -> A}(a) = max_b [ u(A,B) + UTIL_{C -> B}(b) ]
    UTIL_B_to_A = {}  # a -> utility
    ARG_B = {}        # a -> best b
    for a in COLORS:
        best_val = float("-inf")
        best_b = None
        for b in COLORS:
            val = edge_utility(a, b) + UTIL_C_to_B[b]  # A-B + child
            if val > best_val:
                best_val = val
                best_b = b
        UTIL_B_to_A[a] = best_val
        ARG_B[a] = best_b

    # Root A chooses best a
    a_best = max(COLORS, key=lambda a: UTIL_B_to_A[a])

    # Phase 3: VALUE propagation
    b_best = ARG_B[a_best]
    c_best = ARG_C[b_best]
    d_best = ARG_D[c_best]
    e_best = ARG_E[d_best]

    t1 = time.perf_counter()

    # Total utility over chain edges: AB, BC, CD, DE
    total_utility = (
        edge_utility(a_best, b_best) +
        edge_utility(b_best, c_best) +
        edge_utility(c_best, d_best) +
        edge_utility(d_best, e_best)
    )

    print("=== DPOP: chain5 (A-B-C-D-E) ===")
    print(f"d = {len(COLORS)}")
    print("UTIL table sizes:")
    print(f"  |UTIL(E->D)| = {len(UTIL_E_to_D)} (depends on D) = d")
    print(f"  |UTIL(D->C)| = {len(UTIL_D_to_C)} (depends on C) = d")
    print(f"  |UTIL(C->B)| = {len(UTIL_C_to_B)} (depends on B) = d")
    print(f"  |UTIL(B->A)| = {len(UTIL_B_to_A)} (depends on A) = d")
    print(f"Runtime: {(t1 - t0)*1000:.3f} ms\n")

    print("Chosen assignment via VALUE propagation:")
    print(f"  A = {a_best} ({COLOR_NAMES[a_best]})")
    print(f"  B = {b_best} ({COLOR_NAMES[b_best]})")
    print(f"  C = {c_best} ({COLOR_NAMES[c_best]})")
    print(f"  D = {d_best} ({COLOR_NAMES[d_best]})")
    print(f"  E = {e_best} ({COLOR_NAMES[e_best]})\n")

    print(f"Total utility (sum over edges AB, BC, CD, DE) = {total_utility}")


if __name__ == "__main__":
    main()
