# dpop_triangle.py
# DPOP example: 3-node triangle graph coloring problem (A-B-C-A)
# Pseudotree : A -> B -> C, with back-edge C -> A
# P(C)=B, PP(C) = {A} => UTIL_C_to_B depends on (A, B)

import time

COLORS = [0, 1, 2]  # 3 colors
COLOR_NAMES = ["Red", "Green", "Blue"]  # must match len(COLORS)


def edge_utility(x, y):
    """Utility for an edge constraint: 0 if colors differ, -1 if same."""
    return -1 if x == y else 0


def main():
    t0 = time.perf_counter()

    # Phase 2: UTIL propagation
    # UTIL_{C -> B}(a, b) = max_c [ u(B, C) + u(A, C) ]
    UTIL_C_to_B = {}  # (a, b) -> utility
    ARG_C = {}        # (a, b) -> best c achieving that utility

    for a in COLORS:
        for b in COLORS:
            best_val = float("-inf")
            best_c = None
            for c in COLORS:
                val = edge_utility(b, c) + edge_utility(c, a)
                if val > best_val:
                    best_val = val
                    best_c = c
            UTIL_C_to_B[(a, b)] = best_val
            ARG_C[(a, b)] = best_c

    # UTIL_{B -> A}(a) = max_b [ u(A, B) + UTIL_{C -> B}(a, b) ]
    UTIL_B_to_A = {}  # a -> utility
    ARG_B = {}        # a -> best b achieving that utility

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

    t1 = time.perf_counter()

    total_utility = (
        edge_utility(a_best, b_best) +
        edge_utility(b_best, c_best) +
        edge_utility(c_best, a_best)
    )

    
    print("=== DPOP: triangle (A-B-C-A) ===")
    print(f"d = {len(COLORS)}")
    print("UTIL table sizes:")
    print(f"  |UTIL(C->B)| = {len(UTIL_C_to_B)} (depends on A,B) = d^2")
    print(f"  |UTIL(B->A)| = {len(UTIL_B_to_A)} (depends on A)   = d")
    print(f"Runtime: {(t1 - t0)*1000:.3f} ms\n")

    print("Chosen assignment via VALUE propagation:")
    print(f"  A = {a_best} ({COLOR_NAMES[a_best]})")
    print(f"  B = {b_best} ({COLOR_NAMES[b_best]})")
    print(f"  C = {c_best} ({COLOR_NAMES[c_best]})\n")

    print(f"Total utility (sum over edges AB, BC, CA) = {total_utility}")
   


if __name__ == "__main__":
    main()


