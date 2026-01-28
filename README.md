# Distributed Graph Coloring

This repository contains a Python-based project for studying the **Graph Coloring** problem under different **constraint reasoning frameworks**, ranging from centralized to distributed settings.

The project is developed incrementally as part of an academic assignment and serves both as:
- a **theoretical reference** (problem modeling), and  
- a **practical sandbox** for implementing and comparing algorithms.

---

## Project Goals

The main goal of this repository is to explore how the *same problem* (Graph Coloring) can be formulated and approached under different paradigms:

- **CSP (Constraint Satisfaction Problem)** – centralized formulation  
- **DisCSP (Distributed CSP)** – variables and constraints distributed among agents  
- **DCOP (Distributed Constraint Optimization Problem)** – soft constraints with costs  
- **DPOP** – a distributed algorithm for optimally solving DCOPs  

The implementations start simple and are extended progressively, allowing clear comparisons in terms of modeling, communication, and efficiency.

---

## Scope (Incremental Development)

The repository is intentionally minimal at the beginning and will be expanded gradually.

Planned steps:
- Model Graph Coloring as CSP, DisCSP, and DCOP
- Implement simple baseline solvers (for CSP and DisCSP)
- Implement the DPOP algorithm for the DCOP formulation
- Run small-scale experiments on example graphs
- Compare approaches using basic performance metrics



