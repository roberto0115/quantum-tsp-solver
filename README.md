⚛️ Quantum TSP Solver: Optimización QAOA con PennyLane

Este repositorio contiene una implementación puramente cuántica y orientada a objetos (POO) para resolver el Problema del Viajante (Traveling Salesperson Problem - TSP) utilizando el algoritmo híbrido variacional QAOA (Quantum Approximate Optimization Algorithm).

El proyecto fue desarrollado utilizando el framework PennyLane y demuestra el modelado de principio a fin de un problema NP-Hard: desde la instanciación de un mapa clásico de ciudades, la traducción de las restricciones a un Hamiltoniano de Ising, hasta la mitigación de errores de entrenamiento en el simulador cuántico.

🚀 Características Principales

Arquitectura Modular (POO): El código está estructurado en clases independientes (TSPGraph, TSPHamiltonianBuilder, QAOASolver), separando claramente el problema clásico, la formulación física y la optimización de Machine Learning.

Formulación Rigurosa QUBO $\rightarrow$ Ising: Mapeo matemático estricto utilizando codificación One-Hot.

Penalizaciones Dinámicas: Uso de multiplicadores de Lagrange dinámicos ($B = 3 \cdot \max(W)$) para penalizar estados inválidos y forzar matrices de permutación reales ("Sudoku Cuántico").

Mitigación de Barren Plateaus: Implementación de inicialización adiabática (ángulos cercanos a cero) para el optimizador Adam, evitando colapsos de gradiente en circuitos profundos.

📂 Estructura del Proyecto

quantum-tsp-solver/
│
├── src/
│   ├── utils/
│   │   ├── graph_generator.py # Clase TSPGraph: Genera matrices de pesos y visualiza el grafo con NetworkX.
│   │   └── qubo_to_ising.py   # Clase TSPHamiltonianBuilder: Construye H0 (Mixer) y H1 (Cost) con penalizaciones.
│   │
│   └── solvers/
│       └── tsp_qaoa.py        # Clase QAOASolver: Entrena el circuito cuántico y muestrea la matriz óptima.
│
└── main.py                    # Pipeline principal que coordina el flujo de datos.


🧠 El Hamiltoniano (La Física del Problema)

La clave del éxito del solver radica en la construcción del Hamiltoniano de Coste ($H_1$), compuesto por dos partes:

$$H_1 = A \cdot H_{\text{distancia}} + B \cdot H_{\text{penalización}}$$

Distancias: Penaliza el coste del viaje entre ciudades.

Penalizaciones: Aplica restricciones severas para evitar que el viajante se "clone" o desaparezca:

Término Lineal: Asigna un castigo base.

Repulsión Cuadrática: Operadores de Pauli $Z \otimes Z$ que penalizan tener más de un '1' en la misma fila (mismo instante temporal) o columna (misma ciudad).

💻 Instalación y Uso

Requisitos

El proyecto requiere Python 3.9+ y las siguientes librerías principales:

pennylane

pennylane-lightning (Recomendado para aceleración)

numpy

networkx y matplotlib (Para visualización)

Ejecución

Para ejecutar el pipeline completo para un mapa de 4 ciudades:

git clone [https://github.com/TU_USUARIO/quantum-tsp-solver.git](https://github.com/TU_USUARIO/quantum-tsp-solver.git)
cd quantum-tsp-solver
python main.py


Resultados Esperados

Al ejecutar main.py, el script generará el problema, entrenará el circuito QAOA y medirá el estado final. Debido a la naturaleza probabilística, la salida mostrará el colapso de la función de onda en los autoestados de mínima energía válidos:

=== TOP 3 ESTADOS MÁS PROBABLES ===
1. Estado: |0000000100000010⟩ | Apariciones: 156 (1.56%)
...
Matriz del Viaje Ganador:
[[0 0 0 0]
 [0 0 0 1]
 [0 0 0 0]
 [0 0 1 0]]


✒️ Autor: Roberto Álvarez Paraja.
Desarrollado durante el periodo de prácticas en CTIC Centro Tecnológico.