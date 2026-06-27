# Projeto Grafos — Análise de Rede de Correlação entre FIIs

Projeto de análise de redes (grafos) aplicado a Fundos de Investimento Imobiliário (FIIs) brasileiros, utilizando correlação entre retornos para construir grafos temporais e extrair propriedades estruturais como Árvore Geradora Mínima (MST), caminho mínimo (Dijkstra), componentes conexos (DFS) e centralidade de grau.

##  Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes do Python)

##  Instalação

1. **Clone o repositório ou baixe o zip**
   
   - Clonar
   ```bash
   git clone https://github.com/seu-usuario/Projeto-Grafos.git
   cd Projeto-Grafos
   ```
   - Zip
   ```bash
   https://github.com/MatheusVB-Graf/Projeto-Grafos/archive/refs/heads/main.zip
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   ```

   Ative o ambiente virtual:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

##  Como executar

Execute o script principal a partir da raiz do projeto:

```bash
python main.py
```

O programa irá:
1. Baixar/carregar os dados históricos dos FIIs definidos em `LISTA_FIIS`.
2. Calcular os retornos e a matriz de correlação para cada período (ano).
3. Construir os grafos a partir da matriz de correlação, usando o limiar (`LIMIAR`) definido no código.
4. Calcular MST, caminho mínimo (Dijkstra), componentes conexos (DFS) e grau dos verticespara cada período.
5. Gerar gráficos e tabelas, salvos automaticamente em pelo metodos `salvar_resultados` da classe `GrafoTemporal`:
   ```
   resultados/execucao_<timestamp>_limiar_<valor>/ano_<ano>/
   ```

##  Configurações ajustáveis

No arquivo `main.py` (ou onde estiverem definidas as constantes), você pode ajustar:

| Variável | Descrição |
|---|---|
| `LISTA_FIIS` | Lista de tickers dos FIIs a serem analisados (formato `'TICKER11.SA'`) |
| `LIMIAR` | Valor mínimo de correlação para considerar uma ligação entre dois FIIs (entre -1 e 1) |
| `origem` / `destino` | Vértices usados para o cálculo do caminho mínimo (Dijkstra) |


## Como abrir no PyCharm

1. Abra o PyCharm e selecione **File > Open**, depois selecione a pasta raiz do projeto (`Projeto-Grafos`).

2. **Configure o interpretador Python (ambiente virtual):**
   - Vá em **File > Settings** (Windows/Linux) ou **PyCharm > Preferences** (Mac).
   - Navegue até **Project: Projeto-Grafos > Python Interpreter**.
   - Clique na engrenagem  ao lado do interpretador atual e escolha **Add Interpreter > Add Local Interpreter**.
   - Selecione **Existing environment** e aponte para o executável dentro da pasta `venv` criada anteriormente:
     - Windows: `venv\Scripts\python.exe`
     - Linux/Mac: `venv/bin/python`
   - Se ainda não tiver criado o `venv`, você pode deixar o PyCharm criar um novo automaticamente em **New environment using Virtualenv**.

3. **Instale as dependências direto pelo PyCharm (opcional):**
   - Abra o arquivo `requirements.txt` no editor.
   - O PyCharm deve detectar pacotes faltantes e mostrar um aviso no topo do arquivo com um botão **Install requirements** — clique nele.
   - Alternativamente, abra o terminal integrado (**View > Tool Windows > Terminal**) e rode:
     ```bash
     pip install -r requirements.txt
     ```


4. **Execute o projeto:**
   - Clique com o botão direito em `main.py` e selecione **Run 'main'**.
   - Ou abra o arquivo e use o botão  verde no canto superior direito do editor.


## Estrutura do projeto

```
Projeto-Grafos/
├── main.py                          # Script principal de execução
├── requirements.txt                 # Dependências do projeto
├── src/
│   └── fii_grafos/
│       ├── algoritmos/
│       │   └── algoritmos.py        # Implementações de Kruskal, Dijkstra, DFS, etc.
│       ├── grafo.py                 # Classe Grafo
│       └── grafo_temporal.py        # Classe GrafoTemporal
└── README.md
```

##  Saídas geradas

Para cada período analisado, o projeto gera:
- Gráfico da MST (`mst_<ano>.png`)
- Gráfico do caminho mínimo via Dijkstra (`dijkstra_<ano>.png`)
- Tabela/gráfico de componentes conexos via DFS (`dfs_<ano>.png`)
- Ranking de centralidade de grau(`grau_{ano}.png`)




