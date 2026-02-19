# DPOP example: 5-node cycle (C5) with nodes V1..V5
# Edges: (V1-V4), (V4-V3), (V3-V2), (V2-V5), (V5-V1)
#
# Pseudotree (chain): V1 -> V4 -> V3 -> V2 -> V5
# Back-edge: V5 -> V1
#
# Separator sizes with this pseudotree:
# - V5 has parent V2 and pseudo-parent {V1} => UTIL(V5->V2) depends on (V2, V1) => size d^2
# - V2 has parent V3, separator {V1}        => UTIL(V2->V3) depends on (V3, V1) => size d^2
# - V3 has parent V4, separator {V1}        => UTIL(V3->V4) depends on (V4, V1) => size d^2
# - V4 has parent V1, separator {}          => UTIL(V4->V1) depends on (V1)      => size d

import time

COLORS = [0, 1, 2]
COLOR_NAMES = ["Red", "Green", "Blue"]


def edge_utility(x, y):
    """Utility for an edge constraint: 0 if colors differ, -1 if same."""
    return -1 if x == y else 0


def main():
    t0 = time.perf_counter()

    # Leaf V5: parent=V2, pseudo-parent=V1
    # UTIL_{V5 -> V2}(v2, v1) = max_v5 [ u(V2,V5) + u(V1,V5) ]
    UTIL_5_to_2 = {}
    ARG_5 = {}
    for v2 in COLORS:
        for v1 in COLORS:
            best_val = float("-inf")
            best_v5 = None
            for v5 in COLORS:
                val = edge_utility(v2, v5) + edge_utility(v1, v5)
                if val > best_val:
                    best_val = val
                    best_v5 = v5
            UTIL_5_to_2[(v2, v1)] = best_val
            ARG_5[(v2, v1)] = best_v5

    # Node V2: parent=V3, separator={V1}
    # UTIL_{V2 -> V3}(v3, v1) = max_v2 [ u(V3,V2) + UTIL_{V5->V2}(v2,v1) ]
    UTIL_2_to_3 = {}
    ARG_2 = {}
    for v3 in COLORS:
        for v1 in COLORS:
            best_val = float("-inf")
            best_v2 = None
            for v2 in COLORS:
                val = edge_utility(v3, v2) + UTIL_5_to_2[(v2, v1)]
                if val > best_val:
                    best_val = val
                    best_v2 = v2
            UTIL_2_to_3[(v3, v1)] = best_val
            ARG_2[(v3, v1)] = best_v2

    # Node V3: parent=V4, separator={V1}
    # UTIL_{V3 -> V4}(v4, v1) = max_v3 [ u(V4,V3) + UTIL_{V2->V3}(v3,v1) ]
    UTIL_3_to_4 = {}
    ARG_3 = {}
    for v4 in COLORS:
        for v1 in COLORS:
            best_val = float("-inf")
            best_v3 = None
            for v3 in COLORS:
                val = edge_utility(v4, v3) + UTIL_2_to_3[(v3, v1)]
                if val > best_val:
                    best_val = val
                    best_v3 = v3
            UTIL_3_to_4[(v4, v1)] = best_val
            ARG_3[(v4, v1)] = best_v3

    # Node V4: parent=V1
    # UTIL_{V4 -> V1}(v1) = max_v4 [ u(V1,V4) + UTIL_{V3->V4}(v4,v1) ]
    UTIL_4_to_1 = {}
    ARG_4 = {}
    for v1 in COLORS:
        best_val = float("-inf")
        best_v4 = None
        for v4 in COLORS:
            val = edge_utility(v1, v4) + UTIL_3_to_4[(v4, v1)]
            if val > best_val:
                best_val = val
                best_v4 = v4
        UTIL_4_to_1[v1] = best_val
        ARG_4[v1] = best_v4

    # Root V1 chooses best v1
    v1_best = max(COLORS, key=lambda v1: UTIL_4_to_1[v1])

    # VALUE propagation (top-down)
    v4_best = ARG_4[v1_best]
    v3_best = ARG_3[(v4_best, v1_best)]
    v2_best = ARG_2[(v3_best, v1_best)]
    v5_best = ARG_5[(v2_best, v1_best)]

    t1 = time.perf_counter()

    # Total utility over cycle edges:
    # V1-V4, V4-V3, V3-V2, V2-V5, V5-V1
    total_utility = (
        edge_utility(v1_best, v4_best) +
        edge_utility(v4_best, v3_best) +
        edge_utility(v3_best, v2_best) +
        edge_utility(v2_best, v5_best) +
        edge_utility(v5_best, v1_best)
    )

    print("=== DPOP: cycle5 (C5) with nodes V1..V5 ===")
    print(f"d = {len(COLORS)}")
    print("UTIL table sizes:")
    print(f"  |UTIL(V5->V2)| = {len(UTIL_5_to_2)} (depends on V2,V1) = d^2")
    print(f"  |UTIL(V2->V3)| = {len(UTIL_2_to_3)} (depends on V3,V1) = d^2")
    print(f"  |UTIL(V3->V4)| = {len(UTIL_3_to_4)} (depends on V4,V1) = d^2")
    print(f"  |UTIL(V4->V1)| = {len(UTIL_4_to_1)} (depends on V1)    = d")
    print(f"Runtime: {(t1 - t0)*1000:.3f} ms\n")

    print("Chosen assignment via VALUE propagation:")
    print(f"  V1 = {v1_best} ({COLOR_NAMES[v1_best]})")
    print(f"  V2 = {v2_best} ({COLOR_NAMES[v2_best]})")
    print(f"  V3 = {v3_best} ({COLOR_NAMES[v3_best]})")
    print(f"  V4 = {v4_best} ({COLOR_NAMES[v4_best]})")
    print(f"  V5 = {v5_best} ({COLOR_NAMES[v5_best]})\n")

    print(f"Total utility (sum over cycle edges) = {total_utility}")


if __name__ == "__main__":
    main()
