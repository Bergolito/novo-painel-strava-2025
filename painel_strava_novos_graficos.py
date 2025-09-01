# =======================================================
# Imports
# =======================================================
import altair as alt

# =======================================================
# Constantes
# =======================================================

lista_cores_graficos = [
    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d', '#d95b43', '#5bc0de', '#4caf50', '#ffeb3b', '#c497d9',
    '#00BFFF', '#32CD32', '#FF00FF', '#FFA500', '#5A87E8', '#00CED1', '#FF7F50', '#228B22', '#FFD700', '#000080',
    '#FF1493', '#4B0082', '#8A2BE2', '#7FFF00', '#00FFFF', '#008000'
]

# =======================================================
# Gráficos de Barras
# =======================================================

def gera_grafico_barras_campo(df_sumario, titulo, campo):

    grafico = alt.Chart(df_sumario).mark_bar().encode(
        x=alt.X('mes:N', title='Mês'),
        y=alt.Y(f'{campo}:Q', title=titulo),
        tooltip=['mes', campo],      
        color=alt.Color('mes:N', title='Mês')     
    ).properties(
        title=alt.Title(
            text=titulo
        ),
        width=700,
        height=500
    ).interactive() 

    return grafico
