import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import matplotlib.pyplot as plt 

from src.dcop.max_sum import load_instance, max_sum



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--damping", type=float, default=0.5)
    args = parser.parse_args()

    instance = load_instance(args.instance)
    result = max_sum(instance, max_iters=args.iters, damping=args.damping)

    print("\nInstance:", instance.name)
    print("Iterations:", result["iterations"])
    print("Assignment:")
    for node, color in result["assignment"].items():
        print(f"  {node}: {color}")
    print("Conflicts:", result["conflicts"])

    hist = result.get("history_conflicts")
    if hist:
        plt.figure()
        plt.plot(range(len(hist)), hist)
        plt.xlabel("Iteration")
        plt.ylabel("Conflicts")
        plt.title("Max-Sum convergence")
        plt.show()

if __name__ == "__main__":
    main()
