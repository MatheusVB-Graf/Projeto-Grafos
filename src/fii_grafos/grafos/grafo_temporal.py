import networkx as nx
from fii_grafos.algoritmos.algoritmos import dfs,dijkstra,kruskal,centralidade_grau
import matplotlib.pyplot as plt
import os
from datetime import datetime

class GrafoTemp:
    def __init__(self):
        self.grafos = {}
        self.mst = {}
        self.dijk = {}
        self.grau = {}
        self.dfs = {}


    def add_grafo(self,periodo,grafo,origem,destino):
        self.grafos[periodo] = grafo
        self.mst[periodo] = kruskal(grafo.G)
        self.dijk[periodo] = dijkstra(grafo.G, origem, destino)
        self.grau[periodo] = centralidade_grau(grafo.G)
        self.dfs[periodo] = dfs(grafo.G, origem)


    def getGrafo(self,ano):
        return self.grafos[ano].G

    def getMst(self,ano):
        return self.mst[ano]

    def getDfs(self,ano):
        return self.dfs[ano]

    def getDijk(self,ano):
        return self.dijk[ano]

    def getGrau(self,ano):
        return self.grau[ano]

    def plotar_mst(self,ano,pasta_destino):
        arestas, custo_total = self.getMst(ano)
        if custo_total > 0:
            mst = nx.Graph()
            mst.add_edges_from(arestas)

            plt.figure(figsize=(12, 8))

            if nx.is_connected(mst):
                raiz = max(mst.degree, key=lambda x: x[1])[0]
                pos = nx.bfs_layout(mst, start=raiz)
                nx.draw_networkx(mst, pos, with_labels=True, node_color='lightblue',
                                 node_size=1000, font_size=7, edge_color='gray')
            else:
                componentes = list(nx.connected_components(mst))
                pos = {}
                offset_x = 0
                for comp in componentes:
                    sub = mst.subgraph(comp)
                    if len(comp) > 1:
                        raiz = max(sub.degree, key=lambda x: x[1])[0]
                        sub_pos = nx.bfs_layout(sub, start=raiz)
                    else:
                        sub_pos = {list(comp)[0]: (0, 0)}

                    for nodo, (x, y) in sub_pos.items():
                        pos[nodo] = (x + offset_x, y)
                    offset_x += 3

                nx.draw_networkx(mst, pos, with_labels=True, node_color='lightblue',
                                 node_size=1000, font_size=7, edge_color='gray')

            titulo = f"MST {ano} — custo total: {custo_total:.2f}" if ano else f"MST — custo total: {custo_total:.2f}"

            plt.title(titulo,fontsize=14,fontweight ='bold')
            plt.axis('off')
            plt.tight_layout()
            os.makedirs(pasta_destino, exist_ok=True)

            caminho_arquivo = os.path.join(pasta_destino, f"mst_{ano}.png")

            plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
            plt.close()

    def plotar_dijk(self,ano,pasta_destino):
            caminho_arquivo = os.path.join(pasta_destino, f"dijkstra_{ano}.png")

            caminho, custo_total= self.getDijk(ano)
            grafo = self.getGrafo(ano)

            if grafo is None or grafo.number_of_edges() == 0:
                plt.figure(figsize=(12, 8))
                plt.title(f"Dijkstra {ano} — SEM DADOS", fontsize=14, fontweight='bold', color='darkred')
                plt.text(0.5, 0.5, "Não existem dados ou conexões\npara o ano informado.",
                         horizontalalignment='center', verticalalignment='center', fontsize=12, color='gray')
                plt.axis('off')

                os.makedirs(pasta_destino, exist_ok=True)
                plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
                plt.close()
                return

            G = nx.Graph()
            G.add_nodes_from(caminho)

            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G, seed=42)

            nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue',
                             node_size=1000, font_size=7, edge_color='lightgray')

            if caminho and custo_total != 999:
                arestas_caminho = [(caminho[i], caminho[i + 1]) for i in range(len(caminho) - 1)]

                g_caminho = nx.Graph()
                g_caminho.add_edges_from(arestas_caminho)

                nx.draw_networkx(g_caminho, pos, with_labels=True, node_color='#FF5733',
                                 node_size=1000, font_size=7, edge_color='#FF5733', width=4.0)

                titulo = f"Dijkstra {ano} — Caminho de {caminho[0]} até {caminho[-1]} (Custo: {custo_total:.2f})"
            else:
                titulo = f"Dijkstra {ano} — CAMINHO INEXISTENTE (Custo: 999)"


            plt.title(titulo, fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()

            os.makedirs(pasta_destino, exist_ok=True)
            plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
            plt.close()

    def plotar_dfs(self,ano,pasta_destino):
        grafo = self.getGrafo(ano)
        ordem_visitacao = self.getDfs(ano)

        if grafo is None or grafo.number_of_edges() == 0:
            plt.figure(figsize=(12, 8))
            plt.title(f"DFS {ano} — SEM DADOS", fontsize=14, fontweight='bold', color='darkred')
            plt.text(0.5, 0.5, "Não existem dados ou conexões\npara o ano informado.",
                     horizontalalignment='center', verticalalignment='center', fontsize=12, color='gray')
            plt.axis('off')

            os.makedirs(pasta_destino, exist_ok=True)
            plt.savefig(os.path.join(pasta_destino, f"dfs_{ano}.png"), dpi=300, bbox_inches='tight')
            plt.close()
            return

            # 1. Organiza os dados da DFS em colunas (Passo, Código do Ativo, Função)
        dados_tabela = []
        for i, fii in enumerate(ordem_visitacao):
            passo = f"{i + 1}º"
            dados_tabela.append([passo, fii])

        # 2. Configura a figura proporcional ao tamanho da lista
        fig, ax = plt.subplots(figsize=(6, len(ordem_visitacao) * 0.3 + 1))
        ax.axis('off')

        # 3. MODIFICADO: Títulos das colunas reduzidos para duas opções
        colunas_titulos = ["Ordem", "Ativo (FII)"]
        tabela = ax.table(
            cellText=dados_tabela,
            colLabels=colunas_titulos,
            loc='center',
            cellLoc='center'
        )

        tabela.auto_set_font_size(False)
        tabela.set_fontsize(10)
        tabela.scale(1.2, 1.4)

        # 4. Estilização da tabela com as duas colunas
        for (row, col), cell in tabela.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#9B59B6')  # Roxo para o topo
            else:
                # Efeito Zebra alternando linhas
                if row % 2 == 0:
                    cell.set_facecolor('#F8F9F9')

                # Destaca sutilmente a primeira linha (Início) e a última linha (Fim)
                if row == 1:
                    cell.set_facecolor('#EAFAF1')  # Verde suave para o início da DFS
                    cell.set_text_props(weight='bold')
                elif row == len(ordem_visitacao):
                    cell.set_facecolor('#FDEDEC')  # Vermelho suave para o final da DFS
                    cell.set_text_props(weight='bold')

        plt.title(f"Ordem de Visitação do DFS — Ano {ano}\n", fontsize=14, fontweight='bold')
        plt.tight_layout()

        # 5. Salva a tabela limpa como imagem .png
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_destino, f"dfs_{ano}.png")
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.close()

    def plotar_grau(self,ano,pasta_destino):
        idgraus = self.grau.get(ano)

        if not idgraus:
            # Imagem de aviso padrão caso não existam dados de graus para o ano
            plt.figure(figsize=(8, 4))
            plt.title(f"Grau {ano} — SEM DADOS", fontsize=14, fontweight='bold', color='darkred')
            plt.text(0.5, 0.5, "Não existem dados de centralidade para este ano.",
                     horizontalalignment='center', verticalalignment='center', fontsize=12, color='gray')
            plt.axis('off')
            os.makedirs(pasta_destino, exist_ok=True)
            plt.savefig(os.path.join(pasta_destino, f"grau_{ano}.png"), dpi=300, bbox_inches='tight')
            plt.close()
            return

        # 2. MÁGICA: Ordena o dicionário pelo valor (grau) do maior para o menor
        graus_ordenados = sorted(idgraus.items(), key=lambda item: item[1], reverse=True)

        # 3. Organiza os dados para a tabela (Posição, Ativo, Grau)
        dados_tabela = []
        for i, (fii, valor_grau) in enumerate(graus_ordenados):
            posicao = f"{i + 1}º"
            dados_tabela.append([posicao, fii, int(valor_grau)])

        # 4. Configura a figura proporcional à quantidade de ativos
        fig, ax = plt.subplots(figsize=(7, len(dados_tabela) * 0.3 + 1))
        ax.axis('off')

        # 5. Define as 3 colunas da tabela de ranking
        colunas_titulos = ["Posição", "Ativo (FII)", "Grau (Conexões)"]
        tabela = ax.table(
            cellText=dados_tabela,
            colLabels=colunas_titulos,
            loc='center',
            cellLoc='center'
        )

        tabela.auto_set_font_size(False)
        tabela.set_fontsize(10)
        tabela.scale(1.2, 1.4)

        # 6. Estilização da tabela (Cabeçalho azul/escuro e linhas zebradas)
        for (row, col), cell in tabela.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#2C3E50')  # Azul Escuro/Grafite para diferenciar do DFS roxo
            else:
                # Efeito Zebra
                if row % 2 == 0:
                    cell.set_facecolor('#F8F9F9')

                # Destaca em dourado/amarelo suave o 1º colocado (o hub do grafo)
                if row == 1:
                    cell.set_facecolor('#FEF9E7')
                    cell.set_text_props(weight='bold')

        plt.title(f"Ranking de FIIS por Grau — Ano {ano}\n", fontsize=14, fontweight='bold')
        plt.tight_layout()

        # 7. Salva o arquivo de imagem na pasta correspondente
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_destino, f"grau_{ano}.png")
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.close()


    def salvar_resultados(self,ano,pasta_destino):

        pasta_ano = os.path.join(pasta_destino, f"ano_{ano}")

        os.makedirs(pasta_ano, exist_ok=True)

        print(f"    Processando dados do ano {ano}...")

        # --- 1. PLOT DA MST (Kruskal) ---
        try:
            self.plotar_mst(ano, pasta_ano)
            print("       Gráfico MST gerado.")
        except Exception as e:
            print(f"       Erro no gráfico da MST: {e}")


        try:
            self.plotar_dijk(ano,pasta_ano)
            print("       Gráfico Dijkstra gerado.")
        except Exception as e:
            print(f"       Erro no gráfico do Dijkstra: {e}")


        try:
            self.plotar_dfs(ano, pasta_ano)
            print("       Tabela sequencial DFS gerada.")
        except Exception as e:
            print(f"       Erro na tabela da DFS: {e}")


        try:
            self.plotar_grau(ano, pasta_ano)
            print("       Tabela de Ranking de Graus gerada.")
        except Exception as e:
            print(f"       Erro na tabela de Graus: {e}")

        print(f"\n Execução em lote concluída com sucesso! Verifique a pasta '{pasta_ano}'.\n")
