import sys
import os
import pennylane as qml

# Aseguramos que Python encuentre la carpeta 'src' desde la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from utils.graph_generator import TSPGraph
from utils.qubo_to_ising import TSPHamiltonianBuilder
from solvers.tsp_qaoa import QAOASolver

def main():
    print("=====================================================")
    print("   QUANTUM TSP SOLVER (QAOA) - PIPELINE PRINCIPAL    ")
    print("=====================================================")

    m = 5  # Número de ciudades
    
    # 1. GENERACIÓN DEL PROBLEMA CLÁSICO
    print(f"\n[1] Generando mapa para {m} ciudades...")
    mapa = TSPGraph(num_ciudades=m)
    W = mapa.get_matrix()
    print("Matriz de distancias (W):")
    print(W)
    
    # Descomenta la siguiente línea si quieres que muestre el dibujo del grafo antes de empezar
    # mapa.dibujar_grafo() 

    # 2. CONSTRUCCIÓN DEL MODELO CUÁNTICO
    print("\n[2] Construyendo Hamiltonianos de Ising...")
    constructor = TSPHamiltonianBuilder(matriz_pesos=W)
    H0 = constructor.get_mixer_hamiltonian()
    H1 = constructor.get_cost_hamiltonian()


    wires = range(m**2)
    dev_gpu = qml.device("lightning.gpu", wires=wires)
    
    
    # 3. EJECUCIÓN DEL ALGORITMO QAOA
    print("\n[3] Inicializando Solver Cuántico...")
    qaoa_solver = QAOASolver(H0=H0, H1=H1, m=m, p=7, steps=300,stepsize = 0.05, shots=10000,dev=dev_gpu)
    
    # Entrenar el circuito
    qaoa_solver.optimize()
    
    # Extraer y mostrar la ruta final
    matriz_final = qaoa_solver.get_solution_matrix()

    print("\n=====================================================")
    print("                 EJECUCIÓN FINALIZADA                ")
    print("=====================================================")

if __name__ == "__main__":
    main()