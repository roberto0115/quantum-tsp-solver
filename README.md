# ⚛️ Quantum TSP Solver: QAOA & VQE con PennyLane

![Quantum TSP Banner](https://img.shields.io/badge/Quantum-TSP%20Solver-blue?style=for-the-badge&logo=python) ![PennyLane](https://img.shields.io/badge/PennyLane-QML-purple?style=for-the-badge)

Este repositorio contiene una implementación rigurosa y puramente cuántica para resolver el **Problema del Viajante (Traveling Salesperson Problem - TSP)**, un clásico problema de optimización combinatoria NP-Hard. El proyecto utiliza algoritmos híbridos variacionales, centrándose especialmente en el **QAOA (Quantum Approximate Optimization Algorithm)**, desarrollados utilizando el framework [PennyLane](https://pennylane.ai/).

El objetivo principal de este proyecto es demostrar el modelado completo (End-to-End) de un problema topológico en un sistema cuántico: desde la instanciación clásica del grafo y la matriz de adyacencia, pasando por la estricta formulación QUBO a Hamiltonianos de Ising, hasta la ejecución y sintonización fina del circuito variacional cuántico (Quantum Machine Learning).

---

## 🚀 Características y Arquitectura del Proyecto

El proyecto está diseñado bajo los principios de la **Programación Orientada a Objetos (POO)**, garantizando un código modular, escalable e independiente del flujo principal.

1.  **Formulación Rigurosa QUBO $\rightarrow$ Ising:** Mapeo matemático estricto utilizando codificación *One-Hot* ($O(m^2)$ qubits). El sistema garantiza que las restricciones topológicas se traduzcan perfectamente en un paisaje de energía físico.
2.  **Penalizaciones Dinámicas (Lagrange):** Implementación de multiplicadores dinámicos ($B = 3 \cdot \max(W)$) para penalizar rigurosamente los estados inválidos y forzar al estado base cuántico a ser una matriz de permutación válida ("Sudoku Cuántico").
3.  **Solver QAOA (Evolución Simulada):** Implementación del algoritmo variacional QAOA con **inicialización adiabática** (ángulos semilla muy cercanos a cero) para evitar fenómenos de gradientes desvanecientes (*Barren Plateaus*) en los optimizadores clásicos.
4.  **Generación Dinámica de Grafos:** Integración completa con `NetworkX` para generar problemas aleatorios de topología variable y previsualizar la red nodal de distancias.

---

## 📂 Estructura del Repositorio

El código fuente está centralizado en la carpeta `src`, separado funcionalmente:

```text
quantum-tsp-solver/
│
├── README.md                  # Este documento
├── requirements.txt           # Dependencias del proyecto
├── main.py                    # Pipeline de orquestación principal
│
└── src/
    ├── utils/
    │   ├── graph_generator.py # Clase TSPGraph: Genera grafos, matrices y visualizaciones.
    │   └── qubo_to_ising.py   # Clase TSPHamiltonianBuilder: Transforma el coste al modelo Ising.
    │
    └── solvers/
        └── tsp_qaoa.py        # Clase QAOASolver: Entrena el Ansatz y muestrea la función de onda.