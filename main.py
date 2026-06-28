from src.fii_grafos.grafos.grafo import  Grafo
from src.fii_grafos.preprocessamento.yfinance import carregar_dados
from src.fii_grafos.grafos.grafo_temporal import  GrafoTemp
from pathlib import Path
import pandas as pd
import os
from datetime import datetime


DIR_ATUAL = Path(__file__).resolve().parent
DIR_DADOS = DIR_ATUAL / "dados"
DIR_RESULT = "resultados"
LIMIAR = 0.5

if __name__ == "__main__":
   LISTA_FIIS, df = carregar_dados(DIR_DADOS)
   periodo_analisado = GrafoTemp()



   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   dir_execu = os.path.join(DIR_RESULT, f"execucao_{timestamp}_LIMIAR_{LIMIAR}")

   for periodo, dado_anual in df.groupby(pd.Grouper(freq='YE')):
      ano = periodo.strftime('%Y')

      #pegar apenas FIIs que não possuem 20% dos dados anuais faltantes
      limite_pct_ano = 0.20
      faltantes_ano = dado_anual.isna().sum() / len(dado_anual)

      fiis_bons_ano= faltantes_ano[faltantes_ano <= limite_pct_ano].index
      fiis_removidos_ano = faltantes_ano[faltantes_ano > limite_pct_ano].index

      if len(fiis_removidos_ano) > 0:
         print(f"Ano {ano} — FIIs removidos por dados incompletos: {fiis_removidos_ano.tolist()}")

      dado_anual = dado_anual[ fiis_bons_ano]
      retornos_ano = dado_anual.pct_change(fill_method=None).dropna()


      if retornos_ano.empty:
         continue

      fiis_grafo = Grafo()
      fiis_grafo.ini_matrizadj(LISTA_FIIS, retornos_ano.corr(),LIMIAR)
      periodo_analisado.add_grafo(ano,fiis_grafo,LISTA_FIIS[1],LISTA_FIIS[35])
      periodo_analisado.salvar_resultados(ano,dir_execu)




