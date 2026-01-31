## Distributed Graph Coloring

## Introduction
This document develops the theoretical background required for modeling
and solving the Graph Coloring problem under different constraint-based
frameworks, including CSP, DisCSP, and DCOP.

## Constraint Satisfaction Problems (CSP)
A Constraint Satisfaction Problem (CSP) is defined by a set of variables,
a domain for each variable, and a set of constraints restricting the
allowed combinations of values.

In this work, CSPs are introduced only as a baseline formulation.

## Backtracking Search for CSPs
To solve the CSP formulation of the graph coloring problem, we employ a backtracking search algorithm. Backtracking is a depth-first search procedure that incrementally builds a partial assignment of values to variables and abandons assignments as soon as they violate any constraint. 

At each step, an unassigned variable is selected and assigned a value from its domain that is consistent with the current partial assignment. If no such value exists, the algorithm backtracks to the previous decision point and tries an alternative assignment.

Backtracking guarantees completeness for finite CSPs, meaning that it will find a solution if one exists, or correctly report failure otherwise. Its really simple and general, thus, it is commonly used as a baseline approach for solving CSPs and serves as a natural starting point for comparison with distributed and optimization based methods.

## Distributed Constraint Satisfaction Problems (DisCSP)

While CSPs assume a centralized solver with complete knowledge of all variables and constraints, this assumption is often unrealistic in distributed systems. In many scenarios, variables and constraints are naturally distributed among autonomous agents, each with only partial knowledge of the global problem.

Distributed Constrain Satisfaction Problems (DisCSPs) extend the CSP framework by associating variables with agents and requring solutions to be found through coordination and communication among them, rather than through centralized control.

We implement a simplified DisCSP protocol based on agent local views and OK message propagation. The goal is not to provide a complete DisCSP solver, but to illustrate the transition from centralized CSPs to distributed reasoning, building a bridge toward DCOP formulations.

The common goal of all distributed algorithms is to minimize the number of messages required to find a solution. backtracking algorithms are very popular in centralized systems because they require very little memory. In a distributed implementation, however, they may not be the best basis since in backtrack search, control shifts rapidly between different variables.

## DCOP theory (to be done)

## DPOP theory (to be done)

## DPOP (first implementation)
To introduce the DPOP algorithm in a concrete and accessible way, we begin with a minimal implementation on a triangle graph coloring problem. By this, we explicitly demonstrate the core mechanisms of DPOP which are 
pseudootree construction, utility propagation, and value reconstruction.

Problem Setup
The problem consists of a triangle graph with three nodes, each representing an agent responsible for selecting a color from a shared finite domain. The graph coloring constraints are modeled as soft constraints, where assigning the same color to adjacent nodes incurs a negative utility, while different colors incur zero.

Pseudotree Structure
A fixed pseudotree is assumed for this implementation. One node is selected as the root, and the remaining nodes are arranged in a parent-child hierarchy. The remaining edge in the triangle is treated as a back-edge, introducing a pseudo-parent relationship.

UTIL propagation
The implementation computes the UTIL messages defined by DPOP. Starting from the leaf node, the algorithm computes a utility table that summarizes the optimal contribution of the subtree rooted at that node, conditioned on the values of its parent and pseudo-parent. The prosses invlolves, enumerating all possible assignments of context variables, maximizing over the local variable's domain and storing both the resulting utility values and the corresponding optimal assignments. The resulting utility message is multi-dimensional (2 dimensions in our case) since the existence of back-edge and demonstrating how DPOP handles cycles without backtracking.

VALUE propagation
After utility propagation reaches the root, the root agent selects the value that maximizes the global utility. The implementation then performs VALUE propagation, where each agent reconstructs its locally optimal assignment based on the stored optimization decisions from the UTIL phase.


