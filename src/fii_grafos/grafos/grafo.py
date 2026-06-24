import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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

        for i in range(len(fiis_validos)):
            for j in range(i + 1, len(fiis_validos)):
                fii_1 = fiis_validos[i]
                fii_2 = fiis_validos[j]

                r = correlacoes.loc[fii_1, fii_2]

                if pd.notna(r) and r > limiar:
                    distancia = 1 - r  # d(i,j) = 1 - r(i,j)
                    self.add_arestas(fii_1, fii_2, distancia)

    def plot_grafico(self,id):
        posicao = nx.spring_layout(self.G)
        nx.draw(self.G, posicao, with_labels=True, node_color='lightblue', node_size=1200,font_size=7)
        pesos = nx.get_edge_attributes(self.G, 'weight')
        pesos_formatados = {aresta: f"{peso:.2f}" for aresta, peso in pesos.items()}
        nx.draw_networkx_edge_labels(self.G, posicao, edge_labels=pesos_formatados)
        plt.title(id)
        plt.show()




