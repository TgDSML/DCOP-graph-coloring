# Distributed Graph Coloring as a DCOP

This project implements and experimentally evaluates multiple algorithms for solving the **Distributed Constraint Optimization Problem (DCOP)** formulation of the Graph Coloring problem.

The work focuses on both **exact** and **approximate** DCOP algorithms and analyzes their theoretical properties and empirical behavior.

---

## Problem Formulation

We model Graph Coloring as a **Discrete DCOP**:

- **Variables** → Graph nodes  
- **Domain** → Available colors  
- **Constraints** → Binary cost functions between adjacent nodes  
- **Objective** → Minimize total conflict cost  

Cost definition:
- `0` → valid coloring  
- `-1` → conflict (same color on adjacent nodes)



---

## Implemented Algorithms

### Exact Algorithms

#### DPOP (Dynamic Programming Optimization Protocol)
- Pseudo-tree based
- Bottom-up UTIL propagation
- Top-down VALUE propagation
- Complexity: `O(d^w*)`
- Exact and complete

#### ADOPT
- Asynchronous search-based
- Uses bounds and threshold updates
- Exact but message-intensive

#### BnB-ADOPT
- Branch-and-bound improvement over ADOPT
- Prunes search space
- Reduced search overhead

---

### Approximate Algorithms

#### Max-Sum
- Message-passing on Factor Graph
- Iterative cost propagation
- Exact on trees, approximate on loopy graphs
- Polynomial per iteration

#### DCOP-Gibbs
- Stochastic local sampling
- Probability proportional to `exp(-β · cost)`
- Good scalability
- No optimality guarantee

---

## Project Structure

src/
│
├── dpop/
│ ├── triangle.py
│ ├── chain5.py
│ ├── cycle5.py
│ ├── clique4.py
│ ├── clique5.py
│ └── dpop_diamond.py
│
├── dcop/
│ ├── adopt.py
│ ├── adopt_bnb.py
│ ├── max_sum.py
│ └── gibbs.py
│
scripts/
│ ├── run_dpop.py
│ ├── run_adopt.py
│ ├── run_maxsum.py
│ └── run_gibbs.py


---

## Experimental Analysis

We evaluate algorithms on multiple graph topologies.

### Small Structured Graphs (Exact Evaluation)
- Triangle
- Diamond
- Chain5
- Cycle5
- Clique4
- Clique5

Focus:
- UTIL table sizes
- Separator growth
- Induced width impact

---

### Larger Graphs (Scalability Evaluation)
- Grid 5x5
- Random30

Focus:
- Convergence behavior
- Conflict reduction
- Runtime scaling
- Approximate vs Exact trade-offs

---

## Visualization

The project includes:

- Graph visualizations of final assignments  
- Convergence plots (Gibbs & Max-Sum)  
- Conflict analysis across iterations  

---

## How to Run

Example commands:

```bash
python src/dpop/triangle.py
python scripts/run_gibbs.py
python scripts/run_maxsum.py

