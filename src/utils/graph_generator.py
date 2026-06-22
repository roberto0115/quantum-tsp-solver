import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

class TSPGraph:
    """
    Clase para generar, gestionar y visualizar grafos orientados al 
    Problema del Viajante (TSP).
    """

    def __init__(self, num_ciudades: int, semilla: int = 1234):
        """
        Inicializa el grafo del TSP.
        
        Args:
            num_ciudades (int): Número de ciudades (nodos) del mapa (m).
            semilla (int): Semilla para asegurar la reproducibilidad de los pesos.
        """
        self.num_ciudades = num_ciudades
        self.semilla = semilla
        self.W = None
        
        # Generar la matriz al instanciar la clase
        self._generar_matriz_pesos()

    def _generar_matriz_pesos(self) -> None:
        """
        Método interno. Genera una matriz de adyacencia simétrica con 
        costes aleatorios entre 1 y 4. La diagonal principal se mantiene a 0.
        """
        # Bloqueo de semilla para reproducibilidad
        random.seed(self.semilla)
        np.random.seed(self.semilla)
        
        m = self.num_ciudades
        self.W = np.zeros((m, m))
        
        for i in range(m):
            for j in range(i + 1, m):
                peso = random.randint(1, 4)
                self.W[i, j] = peso
                self.W[j, i] = peso

    def get_matrix(self) -> np.ndarray:
        """
        Devuelve la matriz de pesos (W).
        
        Returns:
            np.ndarray: Matriz simétrica de tamaño (m x m) con los costes.
        """
        if self.W is None:
            raise ValueError("La matriz no ha sido inicializada.")
        return self.W

    def get_max_weight(self) -> float:
        """
        Devuelve el coste máximo de la matriz de adyacencia.
        Útil para calcular dinámicamente las penalizaciones (B).
        """
        return np.max(self.W)

    def dibujar_grafo(self) -> None:
        """
        Visualiza el mapa de topológico utilizando NetworkX y Matplotlib.
        Dibuja los nodos (ciudades) y muestra el peso sobre las aristas.
        """
        if self.W is None:
            print("Error: No hay matriz de pesos generada.")
            return

        # NetworkX consume directamente la matriz de NumPy
        G = nx.from_numpy_array(self.W)
        
        # Layout con semilla para que el dibujo no baile entre ejecuciones
        pos = nx.spring_layout(G, seed=self.semilla)
        
        plt.figure(figsize=(6, 6))
        
        # Dibujamos nodos
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', 
                node_size=1000, font_weight='bold', font_size=12)
        
        # Extraemos y dibujamos los pesos (enteros)
        labels = nx.get_edge_attributes(G, 'weight')
        labels = {k: int(v) for k, v in labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
        
        plt.title(f"Problema del Viajante - Mapa de Costos ({self.num_ciudades} ciudades)")
        plt.show()
