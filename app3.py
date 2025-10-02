import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

# CSS para cor de fundo do sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #1c9ea0 !important;
    }
	[data-testid="stAppViewContainer"] {
        background-color: #dcdddf;
    }
	[data-testid="stVerticalBlock"] {
        background-color: #fff;
        border-radius: 8px;
        padding: 8px;
    }	
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar os anos do dataset
df_atividades = pd.read_csv('datasets/predados/atividades_fisicas_todos.csv', sep=',', encoding='utf-8')
anos = sorted(df_atividades['data_ano'].unique(), reverse=True)

with st.sidebar:
    st.title("Painel de Atividades")
    st.write("Lista de Itens")
    ano_selecionado = st.selectbox("Selecione o ano da atividade:", anos)
	
# ====== Topbar ======
with st.container():

    colA, colB, colC = st.columns([2,6,3])
    with colA:
        st.markdown("### LOGO")
        st.caption("Tagline here")
    with colB:
        st.text_input("Pesquisar", placeholder="Pesquisar...", label_visibility="collapsed")
    with colC:
        st.markdown("**📅 15 Mar 2024 • 15:00**")

st.markdown("---")

# ====== Linha 1 ======
with st.container():
	
	## Linha 1 - Gauges
	#- Gauge: Qtd Total de Atividades
	#- Gauge: Distância em Km das Atividades
	#- Gauge: Qtd de Calorias Gastas das Atividades
	#- Gauge: Tempo em min das Atividades
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		st.metric("Qtd Total de Atividades", "70 °F", "1.2 °F")
	with col2:		
		st.metric("Distância em Km", "9 mph", "-8%")
	with col3:
		st.metric("Qtd de Calorias Gastas", "86%", "4%")
	with col4:
		st.metric("Tempo em min", "86%", "4%")

st.markdown("")

# ====== Linha 2 ======
col4, col5 = st.columns(2)

#- Pie/Donut - Atividades por Tipo
#- Barras: Atividades Físicas por Ano
with col4:
	st.subheader("Pie/Donut - Atividades por Tipo")
	fig_pie = px.pie(values=[20,25,55], names=["Vermelho","Azul","Verde"])
	fig_pie.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10))
	st.plotly_chart(fig_pie, use_container_width=True)

# Vertical columns mock
with col5:
	st.subheader("Barras: Atividades Físicas por Ano")
	x = list(range(1,9))
	fig_v = go.Figure()
	fig_v.add_bar(x=x, y=[70,60,55,65,60,62,58,63], name='Azul')
	fig_v.add_bar(x=x, y=[90,95,85,88,92,90,88,91], name='Verde')
	fig_v.add_bar(x=x, y=[80,75,78,76,77,79,74,78], name='Amarelo')
	fig_v.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10), barmode='group')
	st.plotly_chart(fig_v, use_container_width=True)

# ====== Linha 2 ======
col6, col7 = st.columns(2)

#- Ranking das atividades por Tipo
#- Ranking das atividades por Dia da Semana

# Horizontal bar mock
with col6:
	st.subheader("Ranking das Atividades Por Tipo")



# Vertical columns mock
with col7:
	st.subheader("Ranking das Atividades Por Dia Da Semana")

