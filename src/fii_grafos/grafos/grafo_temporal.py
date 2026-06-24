

class GrafoTemp:
    def __init__(self):
        self.grafos = {}

    def add_ano(self,periodo,grafo):
        self.grafos[periodo] = grafo

    def grafico(self, limiar=None):
        import os
        from pyvis.network import Network
        from datetime import datetime

        pasta_base = "resultados"

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Inclui o limiar no nome da pasta, se foi informado
        if limiar is not None:
            nome_pasta = f"{timestamp}_limiar-{limiar}"
        else:
            nome_pasta = timestamp

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

            net = Network(
                height="800px",
                width="100%",
                bgcolor="#ffffff",
                font_color="black",
                notebook=False
            )

            net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=150)

            for no in G.nodes():
                net.add_node(no, label=no, color="#97c2fc")

            for origem, destino, dados in G.edges(data=True):
                peso = dados.get("weight", 1)
                net.add_edge(
                    origem, destino,
                    value=abs(peso),
                    title=f"{peso:.2f}",
                    color="gray"
                )

            caminho_html = os.path.join(pasta_saida, f"grafo_{ano}.html")
            net.write_html(caminho_html)


        print(f"\nTodos os grafos foram salvos na pasta '{pasta_saida}'.")