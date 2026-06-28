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
   - Caso ocorra algum problema nessa parte, tente pelo  [PyCharm](#como-abrir-no-pycharm)
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

4. **Instale as dependências:**
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
5. Gerar e salvar gráficos e tabelas, a partir do metodo`salvar_resultados` da classe `GrafoTemporal`:
   ```
   resultados/execucao_<timestamp>_limiar_<valor>/ano_<ano>/
   ```


## Como abrir no PyCharm

1. Abra o PyCharm e selecione **File > Open**, depois selecione a pasta raiz do projeto (`Projeto-Grafos`).

2. **Configure o interpretador Python (ambiente virtual no PyCharm):**

   **Acessando as configurações:**
   - Olhe para o canto inferior direito do PyCharm. Clique onde está escrito **"No Interpreter"** (ou na versão do Python atual).
   - Selecione **Add New Interpreter > Add Local Interpreter...**
   
   *(Alternativa: Vá no menu superior em **File > Settings** (Windows) ou **PyCharm > Settings** (Mac) > **Python Interpreter** > **Add Interpreter** > **Add Local Interpreter...**)*

   **Criando o ambiente automaticamente:**
   - Na janela que abrir, mantenha a opção *Environment* marcada como **Generate new**.
   - No campo *Type*, selecione **Virtualenv**.
   - No campo *Base Python*, certifique-se de que uma versão do Python (3.10 ou superior) está selecionada.
   - No campo *Location*, o PyCharm já vai sugerir automaticamente a criação de uma pasta terminada em `\venv` dentro do seu projeto. Pode deixar como está.
   - Clique em **OK**. O PyCharm vai criar a pasta e ativar o ambiente sozinho.

3.**Instale as dependências direto pelo PyCharm (opcional):**
   
   **Método Automático (Recomendado):**
   - Abra o arquivo `requirements.txt` no editor do PyCharm.
   - A IDE detectará os pacotes faltantes e exibirá uma barra de aviso no topo. Clique em **Install requirements**.

   **Método Manual (Via Terminal do PyCharm):**
   - Abra o terminal integrado acessando o menu **View > Tool Windows > Terminal** (ou clique em *Terminal* na barra inferior).
   - **Importante:** Certifique-se de que o ambiente virtual esteja ativo. Se não aparecer `(venv)` antes do seu nome no terminal, ative-o com o comando correspondente ao seu sistema operacional:
     - Windows: `.venv\Scripts\activate`
     - Linux/Mac: `source venv/bin/activate`
   - Com o ambiente ativo, execute o comando para instalar os pacotes:
     ```bash
     pip install -r requirements.txt
     ```

4. **Execute o projeto:**

    ```bash
     python ./main.py
     ``` 

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
##  Configurações ajustáveis

No arquivo `main.py` (ou onde estiverem definidas as constantes), você pode ajustar:

| Variável | Descrição |
|---|---|
| `LISTA_FIIS` | Lista de tickers dos FIIs a serem analisados (formato `'TICKER11.SA'`) |
| `LIMIAR` | Valor mínimo de correlação para considerar uma ligação entre dois FIIs (entre -1 e 1) |
| `origem` / `destino` | Vértices usados para o cálculo do caminho mínimo (Dijkstra) |


##  Saídas geradas

Para cada período analisado, o projeto gera:
- Gráfico da MST (`mst_<ano>.png`)
- Gráfico do caminho mínimo via Dijkstra (`dijkstra_<ano>.png`)
- Tabela/gráfico de componentes conexos via DFS (`dfs_<ano>.png`)
- Ranking de centralidade de grau(`grau_{ano}.png`)




