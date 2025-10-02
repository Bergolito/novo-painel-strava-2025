# app.py
# Dashboard estilo "Jira" para dataset de atividades (ou dados de exemplo)
# Rodar: streamlit run app.py

import io
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard de Atividades", layout="wide")

# -----------------------------
# Carregamento de dados
# -----------------------------
@st.cache_data
def load_csv(file_bytes: bytes | None):
    if file_bytes:
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        # Tenta carregar um arquivo local chamado atividades.csv, se existir
        try:
            df = pd.read_csv("atividades.csv")
        except Exception:
            df = None
    return df

def make_demo_data(n=500, seed=42):
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2024-01-01")
    dates = start + pd.to_timedelta(rng.integers(0, 500, size=n), unit="D")
    types = rng.choice(["Run", "Walk", "Workout", "Weight Training", "Ride"], size=n, p=[0.32, 0.35, 0.15, 0.1, 0.08])
    distance = np.round(np.where(types=="Run", rng.normal(6, 2, n), np.where(types=="Ride", rng.normal(20,8,n), rng.normal(2,1,n))), 2)
    distance = np.clip(distance, 0, None)
    elapsed = np.clip(np.round(distance * rng.normal(8, 2, n) + rng.normal(10, 5, n)), 5, None)  # minutos
    calories = np.clip(np.round(distance * rng.normal(70, 20, n) + rng.normal(100, 50, n)), 30, None)

    df = pd.DataFrame({
        "Activity ID": np.arange(1, n+1),
        "Activity Date": dates,
        "Activity Type": types,
        "Distance": distance,          # km
        "Elapsed Time": elapsed,       # min
        "Calories": calories,          # kcal
        "Relative Effort": rng.normal(40, 10, n)
    })
    return df

uploaded = st.sidebar.file_uploader("Envie seu arquivo atividades.csv", type=["csv"])
#df = load_csv(uploaded.read() if uploaded else None)
df = pd.read_csv('datasets/atividades.csv', sep=',', encoding="ISO-8859-1")

if df is None:
    st.info("Não encontrei `atividades.csv`. Usando **dados de exemplo** para demonstrar o dashboard.")
    df = make_demo_data()

# -----------------------------
# Normalização de colunas
# -----------------------------
# Garante nomes esperados
cols = df.columns.str.strip()
df.columns = cols

# Datas
if "Activity Date" in df.columns:
    df["Activity Date"] = pd.to_datetime(df["Activity Date"], errors="coerce")
else:
    st.error("Coluna 'Activity Date' não encontrada no CSV.")
    st.stop()

# Métricas (com fallback)
if "Distance" not in df.columns:
    df["Distance"] = 0.0
if "Elapsed Time" not in df.columns:
    df["Elapsed Time"] = 0.0
if "Calories" not in df.columns:
    df["Calories"] = np.nan
if "Activity Type" not in df.columns:
    df["Activity Type"] = "Desconhecida"

df["week"] = df["Activity Date"].dt.to_period("W").apply(lambda p: p.start_time)
df["year"] = df["Activity Date"].dt.year

# -----------------------------
# Filtros (sidebar)
# -----------------------------
min_date = pd.to_datetime(df["Activity Date"].min())
max_date = pd.to_datetime(df["Activity Date"].max())
st.sidebar.markdown("### Filtros")

date_range = st.sidebar.date_input(
    "Período",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date()
)

types_avail = sorted(df["Activity Type"].fillna("Desconhecida").unique().tolist())
types_sel = st.sidebar.multiselect("Tipos de atividade", types_avail, default=types_avail)

# Meta simples para “risco”
meta_dist_km = st.sidebar.number_input("Meta de distância por atividade (km)", min_value=0.0, value=5.0, step=0.5)

# Aplica filtros
mask_date = (df["Activity Date"].dt.date >= date_range[0]) & (df["Activity Date"].dt.date <= date_range[-1])
mask_type = df["Activity Type"].isin(types_sel)
fdf = df[mask_date & mask_type].copy()

# -----------------------------
# KPIs (cards)
# -----------------------------
total_ativ = int(fdf.shape[0])
dist_total = float(np.nansum(fdf["Distance"]))
tempo_total_h = float(np.nansum(fdf["Elapsed Time"]) / 60.0)
cal_total = float(np.nansum(fdf["Calories"])) if fdf["Calories"].notna().any() else np.nan

# Layout superior: 4 cards
st.markdown("## Demo Dashboard")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de Atividades", f"{total_ativ:,}".replace(",", "."))
c2.metric("Distância Total", f"{dist_total:,.1f} km".replace(",", "."))
c3.metric("Tempo Total", f"{tempo_total_h:,.1f} h".replace(",", "."))
c4.metric("Calorias", f"{cal_total:,.0f} kcal".replace(",", ".")) if not np.isnan(cal_total) else c4.metric("Calorias", "—")

st.caption("Use os filtros na barra lateral para refinar o período, tipos de atividade e meta.")

# -----------------------------
# Linha do meio: Barras empilhadas (contagem por semana e tipo)
# -----------------------------
mid_left, mid_mid, mid_right = st.columns([1.4, 1.2, 1.2])

# Barras empilhadas
weekly_counts = (
    fdf.groupby(["week", "Activity Type"], dropna=False)
       .size()
       .reset_index(name="Qtde")
       .sort_values("week")
)
fig_bar = px.bar(
    weekly_counts, x="week", y="Qtde", color="Activity Type",
    title="Contagem de atividades por semana",
    labels={"week": "Semana", "Qtde": "Qtd."},
)
fig_bar.update_layout(margin=dict(l=10, r=10, t=50, b=10), legend_title_text="Tipo")
mid_left.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# Pizza / Do-nut por tipo
# -----------------------------
share = (
    fdf["Activity Type"].fillna("Desconhecida").value_counts()
    .reset_index()
    .rename(columns={"index": "Activity Type", "Activity Type": "Qtde"})
)

labels = ['Apples', 'Oranges', 'Bananas', 'Grapes']
values = [30, 20, 15, 35]

# Create the pie chart
#fig = px.pie(names=labels, values=values, title='Fruit Distribution')

fig_pie = px.pie(
    share, names=labels, values=values,
    hole=0.55, title="Proporção por tipo de atividade"
)
fig_pie.update_layout(margin=dict(l=10, r=10, t=50, b=10))
mid_mid.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Gauge: Itens em risco (%)
# Definição simples: atividades com distância < meta_dist_km
# -----------------------------
if fdf.empty:
    pct_risco = 0.0
else:
    itens_risco = (fdf["Distance"] < meta_dist_km).sum()
    pct_risco = 100.0 * itens_risco / len(fdf)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=pct_risco,
    number={'suffix': "%"},
    title={'text': "Itens em Risco"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'thickness': 0.25},
        'steps': [
            {'range': [0, 60], 'color': "#e5f5e0"},
            {'range': [60, 85], 'color': "#fee6ce"},
            {'range': [85, 100], 'color': "#fdd0a2"},
        ],
        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': pct_risco}
    }
))
fig_gauge.update_layout(margin=dict(l=10, r=10, t=50, b=10))
mid_right.plotly_chart(fig_gauge, use_container_width=True)

# -----------------------------
# Linha inferior: distância mensal e tabela
# -----------------------------
bot_left, bot_right = st.columns([1.4, 1.6])

monthly = (
    fdf.assign(year_month=fdf["Activity Date"].dt.to_period("M").dt.to_timestamp())
       .groupby("year_month")
       .agg(Dist_km=("Distance", "sum"),
            Tempo_min=("Elapsed Time", "sum"),
            Calorias=("Calories", "sum"))
       .reset_index()
)
if not monthly.empty:
    fig_line = px.line(
        monthly, x="year_month", y="Dist_km",
        markers=True, title="Evolução da distância mensal (km)",
        labels={"year_month": "Mês", "Dist_km": "Distância (km)"}
    )
    fig_line.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    bot_left.plotly_chart(fig_line, use_container_width=True)

# Tabela (últimos 12 meses)
st.markdown("---")
st.subheader("Resumo (últimos 12 meses)")
if not monthly.empty:
    last12 = monthly.sort_values("year_month").tail(12)
    last12["Tempo_h"] = (last12["Tempo_min"] / 60.0).round(1)
    show = last12[["year_month", "Dist_km", "Tempo_h", "Calorias"]].rename(
        columns={"year_month": "Mês", "Dist_km": "Distância (km)", "Tempo_h": "Tempo (h)"}
    )
    st.dataframe(show, use_container_width=True, hide_index=True)
else:
    st.info("Sem dados no período selecionado.")

# -----------------------------
# Rodapé
# -----------------------------
st.caption("⚙️ Dica: ajuste a 'Meta de distância por atividade' na barra lateral para alterar o cálculo dos 'Itens em Risco'.")
