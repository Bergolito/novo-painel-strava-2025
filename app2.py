
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="Dashboard", layout="wide")

# (230, 255, 251)
# Color: rgb(230, 255, 251)
# Color: rgb(230, 255, 251)
# CSS para cor de fundo do sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #1c9ea0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("Menu Lateral")
    st.write("Conteúdo do sidebar aqui")
    st.button("Botão exemplo")
	
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

# ====== NOVO ======
with st.container():
	
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

# ====== KPIs ======
col1, col2, col3 = st.columns(3)
with col1:
	st.metric(label="Lorem Ipsum", value="500%", delta="▲")
	st.progress(0.68)
with col2:
	st.metric(label="Lorem Ipsum", value="120%", delta="▼")
	st.progress(0.83)
with col3:
	st.metric(label="Lorem Ipsum", value="350%", delta="+")
	st.progress(0.90)


st.markdown("")


# ====== Charts Row ======
col4, col5, col6 = st.columns(3)

# Horizontal bar mock
with col4:
	st.subheader("Lorem Ipsum")
	df_bars = px.data.tips().head(6)
	fig_h = go.Figure()
	fig_h.add_bar(y=["A","B","C","D","E","F"], x=[23,27,18,31,21,26], orientation='h', name='Azul')
	fig_h.add_bar(y=["A","B","C","D","E","F"], x=[28,32,20,35,24,29], orientation='h', name='Amarelo')
	fig_h.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10), barmode='group')
	st.plotly_chart(fig_h, use_container_width=True)
	st.caption("Legenda: Azul / Amarelo")


# Vertical columns mock
with col5:
	st.subheader("Lorem Ipsum")
	x = list(range(1,9))
	fig_v = go.Figure()
	fig_v.add_bar(x=x, y=[70,60,55,65,60,62,58,63], name='Azul')
	fig_v.add_bar(x=x, y=[90,95,85,88,92,90,88,91], name='Verde')
	fig_v.add_bar(x=x, y=[80,75,78,76,77,79,74,78], name='Amarelo')
	fig_v.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10), barmode='group')
	st.plotly_chart(fig_v, use_container_width=True)


# Pie mock
with col6:
	st.subheader("Lorem Ipsum")
	fig_pie = px.pie(values=[20,25,55], names=["Vermelho","Azul","Verde"])
	fig_pie.update_layout(height=260, margin=dict(l=10,r=10,t=10,b=10))
	st.plotly_chart(fig_pie, use_container_width=True)


# ====== Progress Row ======
col7, col8, col9 = st.columns(3)
for c, pct in zip([col7,col8,col9],[0.65,0.55,0.78]):
	with c:
		st.subheader("Lorem Ipsum")
		st.success("Lorem ipsum is simply dummy text")