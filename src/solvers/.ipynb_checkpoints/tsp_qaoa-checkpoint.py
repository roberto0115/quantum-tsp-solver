import pennylane as qml
from pennylane import numpy as np
import os
import sys

# Añadimos la carpeta 'src' al path para poder importar las utilidades
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.graph_generator import TSPGraph
from utils.qubo_to_ising import TSPHamiltonianBuilder

class QAOASolver:
    """
    Clase dedicada exclusivamente a ejecutar el algoritmo QAOA para encontrar 
    el autoestado de mínima energía de un Hamiltoniano dado.
    """

    def __init__(self, H0, H1, m: int, dev: qml.device,p: int = 4, steps: int = 200,stepsize: float = 0.1, shots: int = 10000):
        """
        Inicializa el solver de QAOA.
        
        Args:
            H0: Hamiltoniano Mezclador (Mixer Hamiltonian).
            H1: Hamiltoniano de Coste (Cost Hamiltonian).
            m (int): Número de ciudades (necesario para dar formato a la matriz final).
            p (int): Profundidad del circuito QAOA (capas).
            steps (int): Pasos de entrenamiento del optimizador Adam.
            shots (int): Número de mediciones/muestreos al final del circuito.
            dev: Penylane device
        """
        self.H0 = H0
        self.H1 = H1
        self.m = m
        self.num_qubits = m ** 2
        self.p = p
        self.steps = steps
        self.stepsize = stepsize
        self.shots = shots
        
        self.wires = range(self.num_qubits)
        self.dev = dev
        self.angles_optimos = None

    def optimize(self):
        """
        Ejecuta el entrenamiento variacional de QAOA para minimizar la energía del Hamiltoniano H1.
        """
        print(f"\n--- Entrenando QAOA (Profundidad: {self.p}, Pasos: {self.steps}, StepSize: {self.stepsize}) ---, device: {self.dev}")
        
        @qml.qnode(self.dev)
        def energy(angles):
            for w in self.wires:
                qml.Hadamard(wires=w)
            for i in range(self.p):
                qml.qaoa.cost_layer(angles[2*i+1], self.H1)
                qml.qaoa.mixer_layer(angles[2*i], self.H0)
            return qml.expval(self.H1)

        # Inicialización adiabática (cercana a cero) para evitar Barren Plateaus
        angles = np.array([0.01] * (2 * self.p), requires_grad=True)
        optimizer = qml.AdamOptimizer(stepsize=self.stepsize)

        for i in range(self.steps):
            angles, current_energy = optimizer.step_and_cost(energy, angles)
            
            if (i + 1) % 50 == 0:
                print(f"  Paso {i+1:3d} | Energía: {current_energy:.4f}")
                
        self.angles_optimos = angles
        print(f"\nÁngulos óptimos encontrados:\n{self.angles_optimos}")
        return self.angles_optimos

    def get_solution_matrix(self):
        """
        Muestrea el circuito con los ángulos óptimos encontrados y extrae
        el estado más probable, devolviéndolo con formato de matriz de viaje.
        """
        if self.angles_optimos is None:
            raise ValueError("Debes ejecutar el método optimize() antes de pedir la solución.")

        print("\n--- Muestreando el estado cuántico final ---")
        
        @qml.qnode(self.dev)
        def sample_solutions(angles):
            for w in self.wires:
                qml.Hadamard(wires=w)
            for i in range(self.p):
                qml.qaoa.cost_layer(angles[2*i+1], self.H1)
                qml.qaoa.mixer_layer(angles[2*i], self.H0)
            return qml.sample()

        muestras = sample_solutions(self.angles_optimos, shots=self.shots)

        # ANÁLISIS ESTADÍSTICO DE LAS RUTAS
        estados_unicos, conteos = np.unique(muestras, axis=0, return_counts=True)
        indices_ordenados = np.argsort(conteos)[::-1]

        print("\n=== TOP 3 ESTADOS MÁS PROBABLES ===")
        for i in range(min(3, len(estados_unicos))):
            idx = indices_ordenados[i]
            estado = estados_unicos[idx]
            apariciones = conteos[idx]
            porcentaje = (apariciones / self.shots) * 100
            
            estado_str = "".join(map(str, estado))
            print(f"{i+1}. Estado: |{estado_str}⟩ | Apariciones: {apariciones} ({porcentaje:.2f}%)")

        # EXTRACCIÓN DE LA RUTA GANADORA
        indice_ganador = indices_ordenados[0]
        estado_ganador = estados_unicos[indice_ganador]

        print("\nMatriz del Viaje Ganador (Formato Temporal x Ciudades):")
        matriz_viaje = estado_ganador.reshape((self.m, self.m))
        print(matriz_viaje)
        
        return matriz_viaje

