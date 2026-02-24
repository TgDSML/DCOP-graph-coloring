import argparse
import os
import sys
import matplotlib.pyplot as plt
import statistics

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.dcop.max_sum import load_instance
from src.dcop.gibbs import dcop_gibbs, visualize_solution



import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 120,
    "savefig.dpi": 200,

    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.labelweight": "bold",

    "legend.fontsize": 11,
    "lines.linewidth": 2.5,

    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.6,
})

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--instance", required=True)
    p.add_argument("--iters", type=int, default=2000)
    p.add_argument("--beta", type=float, default=2.0)
    p.add_argument("--seeds", type=int, default=10, help="number of seeds (0..seeds-1)")
    p.add_argument("--schedule", choices=["random", "round_robin"], default="random")
    p.add_argument("--plot_seed", type=int, default=0, help="which seed to plot")
    args = p.parse_args()

    inst = load_instance(args.instance)

    results = []
    iters_success = []
    best_conflicts_all = []

    for seed in range(args.seeds):
        res = dcop_gibbs(
            inst,
            max_iters=args.iters,
            beta=args.beta,
            seed=seed,
            schedule=args.schedule
        )
        results.append(res)
        best_conflicts_all.append(res["conflicts"])

        if res["iters_to_zero"] is not None:
            iters_success.append(res["iters_to_zero"])

    success_count = len(iters_success)
    success_rate = success_count / args.seeds

    print("\nInstance:", inst.name)
    print("Runs (seeds):", args.seeds)
    print("Beta:", args.beta)
    print("Max iters:", args.iters)
    print("Schedule:", args.schedule)

    print("\nSuccess rate (0 conflicts):", f"{success_count}/{args.seeds} = {success_rate:.2f}")

    if success_count > 0:
        print("Iterations to reach 0 conflicts (successful runs):")
        print("  mean:", round(statistics.mean(iters_success), 2))
        print("  min :", min(iters_success))
        print("  max :", max(iters_success))
    else:
        print("No successful runs reached 0 conflicts within max_iters.")

    print("\nBest conflicts after run (all seeds):")
    print("  mean:", round(statistics.mean(best_conflicts_all), 2))
    print("  min :", min(best_conflicts_all))
    print("  max :", max(best_conflicts_all))

    # Plot + visualize ONLY for one chosen seed
    plot_seed = args.plot_seed
    if 0 <= plot_seed < args.seeds:
        hist = results[plot_seed]["history_best"]

        print(f"\nAssignment (seed={plot_seed}):")
        assignment = results[plot_seed]["assignment"]
        for node in sorted(assignment.keys()):
            print(f"  {node}: {assignment[node]}")

        
        visualize_solution(
            inst,
            assignment,
            f"Gibbs | {inst.name} | seed={plot_seed} | conflicts={results[plot_seed]['conflicts']}"
        )

        
        plt.figure()

        iters = list(range(len(hist)))

        plt.plot(iters, hist,
                label="DCOP-Gibbs (Best-so-far)",
                alpha=0.9)

        plt.scatter([iters[-1]], [hist[-1]], s=50, zorder=5)

        plt.title(f"Σύγκλιση (Convergence): {inst.name} | DCOP-Gibbs")
        plt.xlabel("Αριθμός Επαναλήψεων (Iterations)")
        plt.ylabel("Αριθμός Συγκρούσεων")

        plt.legend(loc="upper right")
        plt.xlim(0, max(iters[-1], 1))
        plt.ylim(-1, max(hist[0], 1) + 1)

        plt.tight_layout()
        plt.show()    
    


if __name__ == "__main__":
    main()
