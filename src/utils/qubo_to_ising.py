import pennylane as qml
import numpy as np

class TSPHamiltonianBuilder:
    """
    Clase encargada de construir los Hamiltonianos necesarios (Coste y Mezclador)
    para resolver el Problema del Viajante (TSP) usando algoritmos cuánticos.
    Transforma el problema clásico de optimización (QUBO) en un modelo de Ising.
    """

    def __init__(self, matriz_pesos: np.ndarray, A: float = 1.0, B: float = None):
        """
        Inicializa el constructor del Hamiltoniano.
        
        Args:
            matriz_pesos (np.ndarray): La matriz de adyacencia (W) con los costes del grafo.
            A (float): Peso dado a la minimización de la distancia. Por defecto 1.0.
            B (float, opcional): Multiplicador de penalización. Si no se proporciona, 
                                 se calcula automáticamente como 3 * max(W).
        """
        self.W = matriz_pesos
        self.m = matriz_pesos.shape[0]  # El número de ciudades se extrae de la matriz
        self.A = A
        
        # Si no pasamos una constante B, aplicamos la heurística segura por defecto
        self.B = B if B is not None else 3.0 * np.max(self.W)

    def get_mixer_hamiltonian(self):
        """
        Construye el Hamiltoniano Mezclador (H0).
        Aplica un operador Pauli-X a todos los qubits del sistema para 
        permitir la transición entre diferentes estados durante QAOA.
        
        Returns:
            qml.Hamiltonian / operador: El Hamiltoniano H0.
        """
        num_qubits = self.m ** 2
        H0 = sum(qml.PauliX(i) for i in range(num_qubits))
        return H0

    def get_cost_hamiltonian(self):
        """
        Construye el Hamiltoniano de Coste (H1), integrando las distancias 
        del grafo y las penalizaciones para forzar una matriz de permutación válida.
        
        Returns:
            qml.Hamiltonian / operador: El Hamiltoniano H1 (Problema de Ising).
        """
        H1 = 0

        # Penalizaciones relativas a las distancias
        for l in range(self.m):
            l_next = (l + 1) % self.m
            for j in range(self.m):
                for k in range(self.m):
                    if j != k:
                        idx1 = l * self.m + j
                        idx2 = l_next * self.m + k
                        
                        # Añadimos el coste de la arista ponderado por A
                        termino_distancia = (-qml.PauliZ(idx1) - qml.PauliZ(idx2) + (qml.PauliZ(idx1) @ qml.PauliZ(idx2)))
                        H1 += self.A * self.W[j, k] * 0.25 * termino_distancia


        # Penalizaciones relativas a las condiciones del probelma
        coef_lineal = -self.B * (self.m - 2) / 2.0
        coef_cuad = self.B / 2.0


        if coef_lineal != 0: 
            for l in range(self.m):
                for j in range(self.m):
                    idx = l * self.m + j
                    H1 += 2 * coef_lineal * qml.PauliZ(idx)

        for l in range(self.m):
            for j in range(self.m):
                for k in range(j + 1, self.m):
                    idx_j = l * self.m + j
                    idx_k = l * self.m + k
                    H1 += coef_cuad * (qml.PauliZ(idx_j) @ qml.PauliZ(idx_k))

        for j in range(self.m):
            for l in range(self.m):
                for p in range(l + 1, self.m):
                    idx_l = l * self.m + j
                    idx_p = p * self.m + j
                    H1 += coef_cuad * (qml.PauliZ(idx_l) @ qml.PauliZ(idx_p))

        return H1
