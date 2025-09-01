# =======================================================
# Imports
# =======================================================
from datetime import datetime
import pandas as pd

# ==================================
# Funções
# ==================================

# ================================
def sumario_atividades_ano(df_selecionado, ano):
    df_sumario = pd.DataFrame(columns=['mes','qtd','Distance', 'Calories', 'tempo_min'])

    for index, mes in enumerate(range(1, 13)):
        df_novas_atividades = atividades_ano_mes(df_selecionado, ano, mes)
        
        soma_distancia = df_novas_atividades['Distance'].sum()
        soma_calorias = df_novas_atividades['Calories'].sum()
        soma_tempo = df_novas_atividades['tempo_min'].sum()
        df_sumario.loc[index, 'mes'] = mes
        df_sumario.loc[index, 'qtd'] = df_novas_atividades.shape[0]
        df_sumario.loc[index, 'Distance'] = round(soma_distancia,1)
        df_sumario.loc[index, 'Calories'] = round(soma_calorias,1)
        df_sumario.loc[index, 'tempo_min'] = round(soma_tempo,1)

    #df_sumario = df_sumario.rename(columns={'mes': 'Mês', 'qtd': 'Qtd. Atividades', 'Distance': 'Distância (Km)', 'Calories': 'Calorias', 'tempo_min': 'Tempo (min)'})
    return df_sumario
# ================================
def atividades_ano_mes(df_teste, ano, mes):
    colunas_desejadas = ['data_ano', 'data_mes', 'dia_semana', 'Activity Date', 'Activity Name',	'Activity Type', 'Elapsed Time',	'Distance', 'Calories', 'tempo_min']

    novo_df = df_teste[colunas_desejadas]

    novo_df['data'] = pd.to_datetime(novo_df['Activity Date'], format='%b %d, %Y, %I:%M:%S %p').dt.strftime('%d/%m/%Y')

    novo_df = novo_df[(novo_df['data_ano'] == ano) & (novo_df['data_mes'] == mes)]
    
    ordem_colunas = ['data', 'dia_semana', 'Activity Type', 'Activity Name', 'Distance', 'Calories', 'tempo_min']
    novo_df = novo_df[ordem_colunas]

    return novo_df
# ==================================
def obter_mes_por_numero(numero):
  """
  Retorna o nome do mês correspondente ao número fornecido.

  Args:
    numero: Um número inteiro entre 0 e 11, representando um mês (0 = Janeiro, 1 = Fevereiro, ..., 11 = Dezembro).

  Returns:
    O nome do mês correspondente ao número fornecido, ou None se o número for inválido.
  """

  meses = [
      "Janeiro", "Fevereiro", "Março", "Abril",
      "Maio", "Junho", "Julho", "Agosto",
      "Setembro", "Outubro", "Novembro", "Dezembro"
  ]

  if 1 <= numero <= 12:
    return meses[numero-1]
  else:
    return None  # Número inválido
# ==================================