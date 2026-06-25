from src.fii_grafos.grafos.grafo import  Grafo
from src.fii_grafos.preprocessamento.yfinance import carregar_dados
from src.fii_grafos.grafos.grafo_temporal import  GrafoTemp
from pathlib import Path
import pandas as pd


DIR_ATUAL = Path(__file__).resolve().parent
DIR_DADOS = DIR_ATUAL / "dados"
LIMIAR = 0.2

if __name__ == "__main__":
   LISTA_FIIS, df = carregar_dados(DIR_DADOS)
   periodo_analisado = GrafoTemp()

   for periodo, dado_anual in df.groupby(pd.Grouper(freq='YE')):
      ano = periodo.strftime('%Y')

      retornos_ano = dado_anual.pct_change(fill_method=None).dropna()

      if retornos_ano.empty:
         continue
      fiis_grafo = Grafo()
      fiis_grafo.ini_matrizadj(LISTA_FIIS, retornos_ano.corr(),LIMIAR)
      periodo_analisado.add_grafo(ano,fiis_grafo,LISTA_FIIS[0],LISTA_FIIS[8])


   periodo_analisado.grafico(LIMIAR)


