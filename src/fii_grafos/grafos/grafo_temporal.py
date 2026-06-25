import networkx as nx
from fii_grafos.algoritmos.algoritmos import dfs,dijkstra,kruskal,centralidade_grau

class GrafoTemp:
    def __init__(self):
        self.grafos = {}
        self.mst = {}
        self.dijk = {}
        self.grau = {}
        self.dfs = {}

    def dfs(self):
        return nx.dfs_edges(self.G)

    def add_grafo(self,periodo,grafo,origem,destino):
        self.grafos[periodo] = grafo
        self.mst[periodo] = kruskal(grafo.G)
        self.dijk[periodo] = dijkstra(grafo.G, origem, destino)
        self.grau[periodo] = centralidade_grau(grafo.G)
        self.dfs[periodo] = dfs(grafo.G, origem)

    def grafico(self, limiar=None):
        import os
        from datetime import datetime

        pasta_base = "resultados"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        nome_pasta = f"{timestamp}_limiar-{limiar}" if limiar is not None else timestamp
        pasta_saida = os.path.join(pasta_base, nome_pasta)

        quantidade_anos = len(self.grafos)
        if quantidade_anos == 0:
            print("A linha do tempo está vazia!")
            return

        os.makedirs(pasta_saida, exist_ok=True)

        for ano, grafo_obj in self.grafos.items():
            G = grafo_obj.G

            if len(G.nodes) == 0:
                print(f"Ano {ano}: grafo vazio, pulando.")
                continue

            # ---------- grafo principal (com tamanho de nó por grau) ----------
            grau_dict = self.grau.get(ano, {})
            self._grafo_pyvis(
                G, os.path.join(pasta_saida, f"grafo_{ano}.html"),
                grau_dict=grau_dict
            )

            # ---------- MST destacada ----------
            if ano in self.mst:
                arestas_mst = self._extrair_arestas(self.mst[ano])
                self._grafo_pyvis(
                    G, os.path.join(pasta_saida, f"mst_{ano}.html"),
                    arestas_destaque=arestas_mst, cor_destaque="#2ecc71"  # verde
                )

            # ---------- DFS destacada ----------
            if ano in self.dfs:
                arestas_dfs = self._extrair_arestas(self.dfs[ano])
                self._grafo_pyvis(
                    G, os.path.join(pasta_saida, f"dfs_{ano}.html"),
                    arestas_destaque=arestas_dfs, cor_destaque="#e67e22"  # laranja
                )

            # ---------- Gráfico de barras: centralidade de grau ----------
            if grau_dict:
                self._grafico_grau(grau_dict, os.path.join(pasta_saida, f"grau_{ano}.png"))

            # ---------- Heatmap: Dijkstra ----------
            if ano in self.dijk and self.dijk[ano]:
                self._heatmap_dijkstra(self.dijk[ano], os.path.join(pasta_saida, f"dijkstra_{ano}.png"))

        print(f"\nTodos os grafos e gráficos foram salvos na pasta '{pasta_saida}'.")

    def _extrair_arestas(self, dado):
        """Normaliza mst/dfs para uma lista de tuplas (origem, destino),
        aceitando tanto um nx.Graph quanto uma lista de arestas."""
        if hasattr(dado, "edges"):
            return [tuple(sorted((u, v))) for u, v in dado.edges()]
        return [tuple(sorted((u, v))) for u, v in dado]

    def _grafo_pyvis(self, G, caminho_html, grau_dict=None, arestas_destaque=None, cor_destaque="#2ecc71"):
        from pyvis.network import Network

        net = Network(
            height="800px", width="100%",
            bgcolor="#ffffff", font_color="black",
            notebook=False
        )
        net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=150)

        grau_dict = grau_dict or {}
        arestas_destaque = set(arestas_destaque or [])

        for no in G.nodes():
            # tamanho do nó proporcional à centralidade de grau (mín. 10, máx. 50)
            centralidade = grau_dict.get(no, 0)
            tamanho = 10 + centralidade * 40
            net.add_node(no, label=no, color="#97c2fc", size=tamanho,
                         title=f"Centralidade: {centralidade:.3f}")

        for origem, destino, dados in G.edges(data=True):
            peso = dados.get("weight", 1)
            chave = tuple(sorted((origem, destino)))
            em_destaque = chave in arestas_destaque

            net.add_edge(
                origem, destino,
                value=abs(peso),
                title=f"{peso:.2f}",
                color=cor_destaque if em_destaque else "gray",
                width=4 if em_destaque else 1
            )

        net.write_html(caminho_html)

    def _grafico_grau(self, grau_dict, caminho_png, top_n=15):
        import matplotlib.pyplot as plt

        itens = sorted(grau_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
        nos = [str(i[0]) for i in itens]
        valores = [i[1] for i in itens]

        plt.figure(figsize=(10, 6))
        plt.barh(nos, valores, color="#3498db")
        plt.xlabel("Centralidade de grau")
        plt.title(f"Top {top_n} nós por centralidade de grau")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(caminho_png, dpi=150)
        plt.close()

    def _heatmap_dijkstra(self, dijk_dict, caminho_png):
        import matplotlib.pyplot as plt
        import numpy as np

        nos = sorted(dijk_dict.keys())
        matriz = np.full((len(nos), len(nos)), np.nan)

        idx = {no: i for i, no in enumerate(nos)}
        for origem, destinos in dijk_dict.items():
            for destino, dist in destinos.items():
                if destino in idx:
                    matriz[idx[origem], idx[destino]] = dist

        plt.figure(figsize=(8, 7))
        plt.imshow(matriz, cmap="viridis")
        plt.colorbar(label="Distância")
        plt.xticks(range(len(nos)), nos, rotation=90, fontsize=6)
        plt.yticks(range(len(nos)), nos, fontsize=6)
        plt.title("Distâncias mínimas (Dijkstra)")
        plt.tight_layout()
        plt.savefig(caminho_png, dpi=150)
        plt.close()