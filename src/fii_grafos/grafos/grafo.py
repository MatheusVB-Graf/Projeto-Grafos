import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations

class Grafo:
    def __init__(self):
        self.G = nx.Graph()

    def add_vertices(self, listanos):
        self.G.add_nodes_from(listanos)


    def add_arestas(self, origem, destino, peso = 0):
        self.G.add_edge(origem, destino, weight = peso)


    def ini_matrizadj(self,LISTA_FIIS,correlacoes,limiar):
        fiis_validos = [fii for fii in LISTA_FIIS if fii in correlacoes.columns]
        self.add_vertices(fiis_validos)

        for fii_1, fii_2 in combinations(fiis_validos, 2):
            r = correlacoes.loc[fii_1, fii_2]

            if pd.notna(r) and r > limiar:
                distancia = 1 - r
                self.add_arestas(fii_1, fii_2, distancia)


    def getGrafo(self):
        return self.G

