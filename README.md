# ⚛️ Quantum TSP Solver: QAOA & VQE with PennyLane

![Quantum TSP Banner](https://img.shields.io/badge/Quantum-TSP%20Solver-blue?style=for-the-badge&logo=python) ![PennyLane](https://img.shields.io/badge/PennyLane-QML-purple?style=for-the-badge) ![NetworkX](https://img.shields.io/badge/NetworkX-Graphs-lightgrey?style=for-the-badge)

This repository contains a rigorous, purely quantum implementation for solving the **Traveling Salesperson Problem (TSP)**, a classic NP-Hard combinatorial optimization problem. The project leverages hybrid variational quantum algorithms—primarily the **Quantum Approximate Optimization Algorithm (QAOA)**—developed within the [PennyLane](https://pennylane.ai/) quantum machine learning framework.

The primary objective of this project is to demonstrate an end-to-end topological modeling workflow on a quantum system: from classical graph instantiation and adjacency matrix generation, through strict QUBO-to-Ising Hamiltonian mappings, down to the execution and fine-tuning of variational quantum circuits.

---

## 🚀 Key Features & Architecture

The codebase is built on **Object-Oriented Programming (OOP)** principles, ensuring a modular, scalable architecture that separates mathematical formulation from quantum execution.

1.  **Rigorous QUBO $\rightarrow$ Ising Mapping:** Strict mathematical mapping using One-Hot encoding, requiring $O(N^2)$ qubits for an $N$-node graph. The system guarantees that topological constraints are perfectly translated into a physical energy landscape.
2.  **Dynamic Penalty Framework (Lagrange Multipliers):** Implementation of dynamic multipliers ($B = 3 \cdot \max(W)$) to rigorously penalize invalid states. This forces the quantum ground state to represent a valid permutation matrix (the "Quantum Sudoku" constraints).
3.  **QAOA Solver (Simulated Evolution):** Variational execution using QAOA with **adiabatic initialization** (seed angles initialized close to zero). This strategy mitigates vanishing gradients (*Barren Plateaus*) typically encountered by classical optimizers in deep quantum circuits.
4.  **Dynamic Graph Generation:** Seamless integration with `NetworkX` to generate randomized graph topologies, extract adjacency matrices, and visualize nodal distance networks.

---

## 📐 Mathematical Formulation

To embed the TSP into a quantum processing unit, the problem is first formulated as a **Quadratic Unconstrained Binary Optimization (QUBO)** problem, which is then mapped to an **Ising Hamiltonian**. 

The cost function $C(x)$ is defined as:
$$C(x) = \sum_{i,j=1}^{N} W_{ij} \sum_{t=1}^{N} x_{i,t} x_{j, t+1}$$

To ensure a valid tour, hard constraints are applied via penalty terms (Lagrange multipliers):
* **Time Constraint:** Each node is visited exactly once.
* **Space Constraint:** At any given time $t$, the salesperson is at exactly one node.

The resulting Hamiltonian $H = H_{cost} + H_{penalty}$ drives the quantum circuit, where the ground state encodes the optimal route.

---

## 📂 Repository Structure

The source code is centralized within the `src` directory, functionally separated for maintainability:

```text
quantum-tsp-solver/
│
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── main.py                    # Main orchestration pipeline
│
└── src/
    ├── utils/
    │   ├── graph_generator.py # TSPGraph class: Generates graphs, matrices, and viz.
    │   └── qubo_to_ising.py   # TSPHamiltonianBuilder class: QUBO to Ising mapping.
    │
    └── solvers/
        └── tsp_qaoa.py        # QAOASolver class: Ansatz training and wave function sampling.
```
## 👨‍💻 Author
**Roberto Álvarez Paraja**
*Double Degree in Physics and Mathematics, University of Oviedo.*
*Research Project - CTIC Centro Tecnológico (2026).*
