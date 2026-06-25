import networkx as nx

def kruskal(grafo):
    vertices_nomes = list(grafo.nodes())
    matrizG = nx.to_numpy_array(grafo, nodelist=vertices_nomes, weight='weight')
    id_nome = {i: nome for i, nome in enumerate(vertices_nomes)}

    tam = len(matrizG)
    H = []
    T = []
    pai = list(range(tam))
    total = 0

    for v in range(tam):
        for u in range(tam):
            if matrizG[v][u] != 0:
                peso = matrizG[v][u]
                H.append((peso, v, u))
    H.sort()

    pai = list(range(tam))

    for peso, v, u in H:
            if not union(pai, v, u):
                T.append((id_nome[v], id_nome[u]))
                total += peso

    return T, total


def find(pai, v):
    if pai[v] != v:
        pai[v] = find(pai, pai[v])
    return pai[v]


def union(pai, v, u):
    if find(pai, v) != find(pai, u):
        pai[find(pai, v)] = find(pai, u)
        return False
    return True

def dijkstra(grafo, com, fim):
    vertices_nomes = list(grafo.nodes())
    matriz = nx.to_numpy_array(grafo, nodelist=vertices_nomes, weight='weight')
    id_nome = {i: nome for i, nome in enumerate(vertices_nomes)}
    nome_id = {nome: i for i, nome in enumerate(vertices_nomes)}

    com = nome_id[com]
    fim = nome_id[fim]

    tam = len(matriz[0])
    vAbertos = list(range(tam))
    vFechados = []
    custo = {}
    rota = {}

    for v in range(tam):
        custo[v] = 999
        rota[v] = com
    custo[com] = 0

    while vAbertos:
        vMin = vAbertos[0]
        for v in vAbertos:
            if custo[v] < custo[vMin]:
                vMin = v

        vFechados.append(vMin)
        vAbertos.remove(vMin)
        adjs = []
        for adj in vAbertos:
            if matriz[vMin][adj] != 0:
                adjs.append(adj)

        for adj in adjs:
            if custo[vMin] + matriz[vMin][adj] < custo[adj]:
                custo[adj] = custo[vMin] + matriz[vMin][adj]
                rota[adj] = vMin

    caminho = []
    atual = fim
    while (atual != com):
        caminho.append(id_nome[atual])
        atual = rota[atual]
    caminho.append(id_nome[com])
    caminho.reverse()

    return caminho, custo[fim]


def centralidade_grau(grafo):
    vertices_nomes = list(grafo.nodes())
    id_nomes = {i: nome for i, nome in enumerate(vertices_nomes)}
    matrizG = nx.to_numpy_array(grafo, nodelist=vertices_nomes, weight='weight')

    tam = len(matrizG)
    grau = {}
    idgraus = {}

    for i in range(tam):
        grau[i] = 0
        for j in range(tam):
            if matrizG[i][j] != 0:
                grau[i] += 1
    for i in range(tam):
        idgraus[id_nomes[i]] = grau[i]

    return idgraus

def dfs(grafo,inicio):
    vertices_nomes = list(grafo.nodes())
    nome_id = {nome: i for i, nome in enumerate(vertices_nomes)}
    id_nome = {i: nome for i, nome in enumerate(vertices_nomes)}
    matrizG = nx.to_numpy_array(grafo, nodelist=vertices_nomes, weight='weight')

    visitados = []
    pilha = [nome_id[inicio]]
    ordem = []
    while pilha:
        v = pilha.pop()
        if v not in visitados:
            visitados.append(v)
            ordem.append(id_nome[v])
            for vizinho in range(len(matrizG[v])):
                print(vizinho)
                if vizinho not in visitados:
                    pilha.append(vizinho)

    return ordem
