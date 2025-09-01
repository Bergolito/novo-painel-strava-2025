# =======================================================
# Imports
# =======================================================
import pandas as pd
import streamlit as st

from painel_strava_novos_graficos import *
from painel_strava_novas_funcoes import *

# =======================================================
# Datasets
# =======================================================
df_atividades_todos = pd.read_csv('datasets/predados/atividades_fisicas_todos.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2020 = pd.read_csv('datasets/predados/atividades_fisicas_2020.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2021 = pd.read_csv('datasets/predados/atividades_fisicas_2021.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2022 = pd.read_csv('datasets/predados/atividades_fisicas_2022.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2023 = pd.read_csv('datasets/predados/atividades_fisicas_2023.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2024 = pd.read_csv('datasets/predados/atividades_fisicas_2024.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2025 = pd.read_csv('datasets/predados/atividades_fisicas_2025.csv', sep=',', encoding="ISO-8859-1")

df_atividades_simplificado_todos = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_todos.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2020 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2020.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2021 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2021.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2022 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2022.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2023 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2023.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2024 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2024.csv', sep=',', encoding="UTF-8")
df_atividades_simplificado_2025 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2025.csv', sep=',', encoding="ISO-8859-1")

df_sumario_2024 = pd.read_csv('datasets/gerais/sumario_atividades_2024.csv', sep=',', encoding="UTF-8")

df_atvs_tipo_todos = pd.read_csv('datasets/gerais/atividades_geral_por_tipo.csv', sep=',', encoding="UTF-8")
df_atvs_dia_semana_todos = pd.read_csv('datasets/gerais/atividades_geral_por_dia_semana.csv', sep=',', encoding="UTF-8")

df_sumario_atvs_2020 = pd.read_csv('datasets/gerais/sumario_atividades_2020.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2021 = pd.read_csv('datasets/gerais/sumario_atividades_2021.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2022 = pd.read_csv('datasets/gerais/sumario_atividades_2022.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2023 = pd.read_csv('datasets/gerais/sumario_atividades_2023.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2024 = pd.read_csv('datasets/gerais/sumario_atividades_2024.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2025 = pd.read_csv('datasets/gerais/sumario_atividades_2025.csv', sep=',', encoding="UTF-8")

# =======================================================
# Constantes do dashboard
# =======================================================

# CSS para estilizar a tabela
css = """
<style>
.estilo_tabela {
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
}
.estilo_tabela th, .estilo_tabela td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    font-size: 10px;
}
.estilo_tabela th {
    background-color: #008B8B;
    color: #fff;
    font-weight: bold;
    font-size: 10px;
}
.estilo_tabela tr:nth-child(even) {
    background-color: #f9f9f9;
}
</style>
"""

OPCAO_TODOS = 'Todos'
OPCAO_NONE = None
COLUNA_ANO = 'ano'

st.set_page_config(
    page_title="Atividades Físicas Strava",
    page_icon="🏃",

    layout="wide",  # or "centered"
    initial_sidebar_state="expanded",  # or "collapsed"
    menu_items={
        'Get Help': 'https://www.streamlit.io/help',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': '# This is a header',
    }
)

# Definir o título fixo para o painel
st.title("Atividades Físicas Bergson (Strava)")

exibir_filtro_periodo_anos = False

with st.sidebar:
    st.header("Filtros:")
    
    ano_selecionado = st.sidebar.selectbox(
        'Qual o ano deseja visualizar?',
        (OPCAO_TODOS,'2025','2024', '2023', '2022', '2021', '2020'), index=1,
        key="ano_selecionado"
    )

    print(f'Ano Selecionado = {ano_selecionado}')

    if 'ano_selecionado' not in st.session_state:
        st.session_state.ano_selecionado = None

# Definição de abas
nova_aba_01, nova_aba_02 = st.tabs(
  [
    "Sumário de Atividades",  
    "Detalhamento das Atividades",
  ]
)

# filtro
df_selecionado = df_atividades_simplificado_2024
ano_selecionado1 = 2025
if st.session_state.ano_selecionado is None:
    df_selecionado = df_atividades_simplificado_2024
else:

    if st.session_state.ano_selecionado == 'Todos':
        ano_selecionado1 = 'Todos'
        df_selecionado = df_atividades_simplificado_todos

    elif st.session_state.ano_selecionado == '2020':
        ano_selecionado1 = 2020
        df_selecionado = df_atividades_simplificado_2020

    elif st.session_state.ano_selecionado == '2021':
        ano_selecionado1 = 2021
        df_selecionado = df_atividades_simplificado_2021    

    elif st.session_state.ano_selecionado == '2022':
        ano_selecionado1 = 2022
        df_selecionado = df_atividades_simplificado_2022    

    elif st.session_state.ano_selecionado == '2023':
        ano_selecionado1 = 2023
        df_selecionado = df_atividades_simplificado_2023    

    elif st.session_state.ano_selecionado == '2024':
        ano_selecionado1 = 2024
        df_selecionado = df_atividades_simplificado_2024    

    elif st.session_state.ano_selecionado == '2025':
        ano_selecionado1 = 2025
        df_selecionado = df_atividades_simplificado_2025    

# ==============================================================================
with nova_aba_01:

    ano_teste = ano_selecionado1
    st.title(f'Ano {ano_teste} - Atividades: {df_selecionado.shape[0]}')

    # Layout em duas colunas para melhor organização
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    row3_col1, row3_col2 = st.columns(2)

    # ==============================================================
    # Função para estilizar o DataFrame
    def style_dataframe(df):
        return df.style.set_table_styles(
            [
                {
                'selector': 'th',
                'props': [
                    ('background-color', '#1E90FF'),
                    ('color', 'white'),
                    ('font-family', 'Arial, sans-serif'),
                    ('font-size', '10px')
                ]
                }, 
                {
                    'selector': 'td, th',
                    'props': [
                        ('border', '2px solid #000000')
                    ]
                }
            ]
        )
    # ==============================================================

    with row1_col1:
        st.title(f'Sumário Atividades Anual: {ano_teste}')
        df_sumario = sumario_atividades_ano(df_selecionado, ano_teste)
        df_estilo = df_sumario.style.format({'Distance': '{:.1f}', 'Calories': '{:.1f}', 'tempo_min': '{:.1f}'})

        qtd_total = df_sumario['qtd'].sum()
        distancia_total = df_sumario['Distance'].sum()
        calorias_total = df_sumario['Calories'].sum()
        tempo_total = df_sumario['tempo_min'].sum()

        df_sumario_com_total = df_sumario.copy()
        index = df_sumario.shape[0]
        df_sumario_com_total.loc[index, 'mes'] = 'TOTAL'
        df_sumario_com_total.loc[index, 'qtd'] = qtd_total
        df_sumario_com_total.loc[index, 'Distance'] = round(distancia_total,1)
        df_sumario_com_total.loc[index, 'Calories'] = round(calorias_total,1)
        df_sumario_com_total.loc[index, 'tempo_min'] = round(tempo_total,1)

        grafico_qtd = gera_grafico_barras_campo(df_sumario, f'Quantidade de Atividades de {ano_teste}', 'qtd')
        grafico_distancia = gera_grafico_barras_campo(df_sumario, f'Distância Total em Km de {ano_teste}', 'Distance')
        grafico_calorias = gera_grafico_barras_campo(df_sumario, f'Calorias Totais Gastas em {ano_teste}', 'Calories')
        grafico_tempo = gera_grafico_barras_campo(df_sumario, f'Tempo Total em Minutos de {ano_teste}', 'tempo_min')

        df_sumario = df_sumario.rename(columns={
            'mes': 'Mês', 
            'qtd': 'Quantidade de Atividades',
            'Distance': 'Distância (km)',
            'Calories': 'Calorias (kcal)',
            'tempo_min': 'Tempo (min)'
        })
        df_html = style_dataframe(df_sumario_com_total)
        st.write(df_html.to_html(), unsafe_allow_html=True)

        st.subheader(f'Quantidade Total: {qtd_total} | Distância Total: {distancia_total:.1f} km | Calorias Total: {calorias_total:.1f} kcal | Tempo Total: {tempo_total:.1f} min')

    with row2_col1:
        st.altair_chart(grafico_qtd, use_container_width=False)       

    with row2_col2:
        st.altair_chart(grafico_distancia, use_container_width=False)

    with row3_col1:
        st.altair_chart(grafico_calorias, use_container_width=False)

    with row3_col2:
        st.altair_chart(grafico_tempo, use_container_width=False)

# ==================================================================
with nova_aba_02:

    ano_teste = ano_selecionado1
    st.title(f'Ano {ano_teste} - Atividades: {df_selecionado.shape[0]}')

    # Layout em duas colunas para melhor organização
    col1, col2 = st.columns(2)

    with col1:    
        for index, mes in enumerate(range(1, 13)):
            df_novas_atividades = atividades_ano_mes(df_selecionado, ano_teste, mes)

            df_novas_atividades_com_total = df_novas_atividades.copy()
            distancia_mes = df_novas_atividades['Distance'].sum()
            calorias_mes = df_novas_atividades['Calories'].sum()
            tempo_mes = df_novas_atividades['tempo_min'].sum()
            qtd_mes = df_novas_atividades.shape[0]

            index = df_novas_atividades.shape[0]
            df_novas_atividades_com_total.loc[index, 'data'] = 'TOTAL'
            df_novas_atividades_com_total.loc[index, 'dia_semana'] = '...'
            df_novas_atividades_com_total.loc[index, 'Activity Type'] = '...'
            df_novas_atividades_com_total.loc[index, 'Activity Name'] = '...'
            df_novas_atividades_com_total.loc[index, 'Distance'] = round(distancia_mes,1)
            df_novas_atividades_com_total.loc[index, 'Calories'] = round(calorias_mes,1)
            df_novas_atividades_com_total.loc[index, 'tempo_min'] = round(tempo_mes,1)

            nome_mes = obter_mes_por_numero(mes)

            if nome_mes is not None:
                st.title(f'Mês: {nome_mes}')
                df_estilo = df_novas_atividades_com_total.style.format({'Distance': '{:.1f}', 'Calories': '{:.1f}', 'tempo_min': '{:.1f}'})

                df_estilo = style_dataframe(df_novas_atividades_com_total)

                st.write(df_estilo.to_html(), unsafe_allow_html=True)

                st.subheader(f'Mês: {nome_mes} | Quantidade: {qtd_mes} | Distância: {distancia_mes:.1f} km | Calorias: {calorias_mes:.1f} kcal | Tempo: {tempo_mes:.1f} min')
    with col2:
        st.title(f'Gráficos do mês de {nome_mes}')

# ==================================================================