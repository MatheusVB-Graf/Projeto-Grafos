import networkx as nx
from src.fii_grafos.algoritmos.algoritmos import dfs,dijkstra,kruskal,centralidade_grau
import matplotlib.pyplot as plt
import os
import textwrap


class GrafoTemp:
    def __init__(self):
        self.grafos = {}
        self.mst = {}
        self.dijk = {}
        self.grau = {}
        self.dfs = {}


    def add_grafo(self,periodo,grafo,origem,destino):
        self.grafos[periodo] = grafo.getGrafo()
        self.mst[periodo] = kruskal(grafo.getGrafo())
        self.dijk[periodo] = dijkstra(grafo.getGrafo(), origem, destino)
        self.grau[periodo] = centralidade_grau(grafo.getGrafo())
        self.dfs[periodo] = dfs(grafo.getGrafo(), origem)


    def getGrafo(self,ano):
        return self.grafos[ano]

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
            pesos = self.getGrafo(ano)
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

            pesos_arvore = {}
            for u, v in mst.edges():
                peso = pesos[u][v].get('weight', None)
                if peso is not None:
                   pesos_arvore[(u, v)] = f"{peso:.2f}"

            nx.draw_networkx_edge_labels(mst, pos, edge_labels=pesos_arvore,
                                         font_size=7, font_color='darkred')

            titulo = f"MST {ano} — custo total: {custo_total:.2f}" if ano else f"MST — custo total: {custo_total:.2f}"
            plt.title(titulo, fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
        else:
                plt.figure(figsize=(12, 8))
                plt.text(0.5, 0.5, f"Não foi possivel gerar arvore",
                         ha='center', va='center', fontsize=20, fontweight='bold', color='gray')
                plt.axis('off')

                titulo = f"Custo total arvore: {custo_total}"

                plt.title(titulo,fontsize=14,fontweight ='bold')
                plt.axis('off')
                plt.tight_layout()

        os.makedirs(pasta_destino, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_destino, f"mst_{ano}.png")

        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.close()

    def plotar_dijk(self, ano, pasta_destino):
            caminho, custo_total, origem, destino = self.getDijk(ano)
            if custo_total > 0 and caminho:
                arestas = list(zip(caminho, caminho[1:]))
                grafo_caminho = nx.Graph()
                grafo_caminho.add_edges_from(arestas)

                plt.figure(figsize=(12, 8))

                if nx.is_connected(grafo_caminho):
                    raiz = max(grafo_caminho.degree, key=lambda x: x[1])[0]
                    pos = nx.bfs_layout(grafo_caminho, start=raiz)
                    nx.draw_networkx(grafo_caminho, pos, with_labels=True, node_color='lightgreen',
                                     node_size=1000, font_size=7, edge_color='gray')
                else:
                    componentes = list(nx.connected_components(grafo_caminho))
                    pos = {}
                    offset_x = 0
                    for comp in componentes:
                        sub = grafo_caminho.subgraph(comp)
                        if len(comp) > 1:
                            raiz = max(sub.degree, key=lambda x: x[1])[0]
                            sub_pos = nx.bfs_layout(sub, start=raiz)
                        else:
                            sub_pos = {list(comp)[0]: (0, 0)}

                        for nodo, (x, y) in sub_pos.items():
                            pos[nodo] = (x + offset_x, y)
                        offset_x += 3

                    nx.draw_networkx(grafo_caminho, pos, with_labels=True, node_color='lightgreen',
                                     node_size=1000, font_size=7, edge_color='gray')


                titulo = f"Caminho mínimo {ano} - {origem} para {destino} — custo total: {custo_total:.2f}" if ano else f"Caminho mínimo — custo total: {custo_total:.2f}"
                plt.title(titulo, fontsize=14, fontweight='bold')
                plt.axis('off')
                plt.tight_layout()

            else:
                plt.figure(figsize=(12, 8))
                plt.text(0.5, 0.5, "Sem caminho encontrado",
                         ha='center', va='center', fontsize=20, fontweight='bold', color='gray')
                plt.axis('off')

                titulo = f"Caminho mínimo {ano} — sem caminho de {origem} para {destino}" if ano else "Caminho mínimo — sem caminho"
                plt.title(titulo, fontsize=14, fontweight='bold')
                plt.tight_layout()

            os.makedirs(pasta_destino, exist_ok=True)
            caminho_arquivo = os.path.join(pasta_destino, f"dijkstra_{ano}.png")
            plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
            plt.close()

    def plotar_dfs(self, ano, pasta_destino):
            G = self.getGrafo(ano)
            componentes = self.getDfs(ano)

            if componentes:
                n_comp = len(componentes)
                largura_max_caracteres = 40

                dados_tabela = []
                alturas_linha = []

                for i, vertices in enumerate(componentes):
                    posicao = f"{i + 1}º"
                    nos_str = ", ".join(map(str, vertices))
                    nos_wrapped = "\n".join(textwrap.wrap(nos_str, width=largura_max_caracteres))
                    dados_tabela.append([posicao, nos_wrapped])
                    alturas_linha.append(max(1, len(textwrap.wrap(nos_str, width=largura_max_caracteres))))


                altura_total = sum(alturas_linha) * 0.3 + 1
                fig, ax = plt.subplots(figsize=(7, altura_total))
                ax.axis('off')

                colunas_titulos = ["Componente", "Nós"]
                tabela = ax.table(
                    cellText=dados_tabela,
                    colLabels=colunas_titulos,
                    loc='center',
                    cellLoc='center'
                )

                tabela.auto_set_font_size(False)
                tabela.set_fontsize(10)
                tabela.scale(1.2, 1.4)

                for (row, col), cell in tabela.get_celld().items():
                    if row == 0:
                        cell.set_text_props(weight='bold', color='white')
                        cell.set_facecolor('#2C3E50')
                    else:

                        n_linhas = alturas_linha[row - 1]
                        cell.set_height(cell.get_height() * n_linhas)

                        if row % 2 == 0:
                            cell.set_facecolor('#F8F9F9')

                        if row == 1:
                            cell.set_facecolor('#FEF9E7')
                            cell.set_text_props(weight='bold')


                titulo = f"Componentes {ano} — {n_comp} componente(s)" if ano else f"Componentes Conexos — {n_comp} componente(s)"

                plt.title(titulo, fontsize=14, fontweight='bold')
                plt.axis('off')
                plt.tight_layout()
                os.makedirs(pasta_destino, exist_ok=True)

                caminho_arquivo = os.path.join(pasta_destino, f"dfs_{ano}.png")

                plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
                plt.close()

    def plotar_grau(self,ano,pasta_destino):
        idgraus = self.grau.get(ano)

        if not idgraus:

            plt.figure(figsize=(8, 4))
            plt.title(f"Grau {ano} — SEM DADOS", fontsize=14, fontweight='bold', color='darkred')
            plt.text(0.5, 0.5, "Não existem dados de centralidade para este ano.",
                     horizontalalignment='center', verticalalignment='center', fontsize=12, color='gray')
            plt.axis('off')
            os.makedirs(pasta_destino, exist_ok=True)
            plt.savefig(os.path.join(pasta_destino, f"grau_{ano}.png"), dpi=300, bbox_inches='tight')
            plt.close()
            return


        graus_ordenados = sorted(idgraus.items(), key=lambda item: item[1], reverse=True)


        dados_tabela = []
        for i, (fii, valor_grau) in enumerate(graus_ordenados):
            posicao = f"{i + 1}º"
            dados_tabela.append([posicao, fii, int(valor_grau)])


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


        for (row, col), cell in tabela.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='white')
                cell.set_facecolor('#2C3E50')
            else:
                # Efeito Zebra
                if row % 2 == 0:
                    cell.set_facecolor('#F8F9F9')


                if row == 1:
                    cell.set_facecolor('#FEF9E7')
                    cell.set_text_props(weight='bold')

        plt.title(f"Ranking de FIIS por Grau — Ano {ano}\n", fontsize=14, fontweight='bold')
        plt.tight_layout()


        os.makedirs(pasta_destino, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_destino, f"grau_{ano}.png")
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.close()

    def salvar_resultados(self,ano,pasta_destino):

        pasta_ano = os.path.join(pasta_destino, f"ano_{ano}")

        os.makedirs(pasta_ano, exist_ok=True)

        print(f"    Processando dados do ano {ano}...")


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
