import pandas as pd
import yfinance as yf
import os
import json

LISTA_FIIS = [
    # --- FIIs de Papel (Recebíveis / CRIs) ---
    'MXRF11.SA', 'KNCR11.SA', 'CPTS11.SA', 'IRDM11.SA', 'KNIP11.SA',
    'VGHF11.SA', 'RECR11.SA', 'HGCR11.SA', 'VRTA11.SA', 'KNSC11.SA',
    'RBRR11.SA', 'ARRI11.SA', 'CPTR11.SA', 'VGIR11.SA', 'CVBI11.SA',
    'MCCI11.SA', 'URPR11.SA', 'HCTR11.SA', 'DEVA11.SA', 'HABT11.SA',
    'BCRI11.SA', 'RBRY11.SA', 'KNHY11.SA', 'OUJP11.SA', 'CACR11.SA',

    # --- FIIs de Tijolo e Híbridos (Imóveis Físicos) ---
    'HGLG11.SA', 'BTLG11.SA', 'XPLG11.SA', 'VILG11.SA', 'LVBI11.SA',
    'BRCO11.SA', 'GGRC11.SA', 'RBRL11.SA', 'ALZR11.SA', 'HGRE11.SA',
    'BRCR11.SA', 'PVBI11.SA', 'JSRE11.SA', 'VINO11.SA', 'XPML11.SA',
    'VISC11.SA', 'HSML11.SA', 'MALL11.SA', 'HGBS11.SA', 'KNRI11.SA',
    'TRXF11.SA', 'HGRU11.SA', 'RBVA11.SA', 'MAXR11.SA',
]

ANALISE_INICIAL = "2023"
ANALISE_FINAL = "2025"
DATA_INICIAL = f"{ANALISE_INICIAL}-01-01"
DATA_FINAL= f"{ANALISE_FINAL}-12-31"
NOME_DOC  = f"FISS-{DATA_INICIAL}-{DATA_FINAL}.csv"
FIIS_ID = F"LISTAFIIS-{DATA_INICIAL}-{DATA_FINAL}.json"
os.makedirs("dados", exist_ok=True)


def verifica_listafiis(ids):

    if not ids.exists():
        with open(ids, 'w') as f:
            json.dump(LISTA_FIIS, f)
        return True


    with open(ids, 'r') as f:
        lista_antiga = json.load(f)

    if set(LISTA_FIIS) != set(lista_antiga):
        with open(ids, 'w') as f:
            json.dump(LISTA_FIIS, f)
        return True

    return False
def tratar_dados(dados):
    df = dados.dropna(axis=1, how='all')

    faltantes = df.isna().sum().sort_values(ascending=False)

    limite_pct = 0.20
    total_linhas = len(df)
    colunas_ruins = faltantes[faltantes > total_linhas * limite_pct].index

    print("Tickers a remover:", colunas_ruins.tolist())
    df = df.drop(columns=colunas_ruins)

    return df

def carregar_dados(dir_dados):

    caminho_arquivo_dados = dir_dados /NOME_DOC
    caminho_arquivos_ids = dir_dados / FIIS_ID

    if verifica_listafiis(caminho_arquivos_ids) or not os.path.exists(caminho_arquivo_dados):
                 print("Arquivo não encontrado. Baixando do Yahoo Finance...")
                 df_raw = yf.download(LISTA_FIIS, start=DATA_INICIAL, end=DATA_FINAL, threads=False, auto_adjust=False)
                 df = df_raw['Adj Close']
                 df_atualizado = tratar_dados(df)
                 df_atualizado.to_csv(caminho_arquivo_dados)
                 print("Download concluído e dados salvos com sucesso!")
    else:
            print("Arquivo encontrado!")

    return LISTA_FIIS, pd.read_csv(caminho_arquivo_dados, index_col=0, parse_dates=True)
