import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_excel('05_contPlanilhas.xlsx')

def show_dashboard():
    st.header("Produto 2.4")
    data_planilhas = load_data()

    # Limpeza dos nomes das colunas
    data_planilhas.columns = data_planilhas.columns.str.strip()

    # Cálculo dos totais
    total_municipios = data_planilhas['Município'].nunique()
    total_assentamentos = len(data_planilhas)
    total_com_planilha = len(data_planilhas[data_planilhas["Planilha de monitoramento"].str.strip() == "Sim"])

    # Layout em colunas para os totais
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de planilhas de município", total_municipios)

    with col2:
        st.metric("2.4.1 Total de planilhas de assentamento", total_assentamentos)

    with col3:
        st.metric("Total de planilhas", total_com_planilha)

    # Gráfico de pizza com planilhas por município
    st.header("Distribuição de Planilhas por Município")

    planilhas_por_municipio = data_planilhas.groupby('Município').size().reset_index()
    planilhas_por_municipio.columns = ['Município', 'Quantidade']

    fig = px.pie(planilhas_por_municipio, 
                 values='Quantidade', 
                 names='Município',
                 title='Distribuição de Planilhas por Município')

    # Atualiza o layout para melhor visualização
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

    # Tabela Completa
    st.header("Tabela Completa")
    st.dataframe(data_planilhas)

    # Filtro por município
    st.header("Filtrar por Município")
    municipio_selecionado = st.selectbox(
        "Selecione um município:",
        options=sorted(data_planilhas["Município"].unique())
    )

    if municipio_selecionado:
        filtered_data = data_planilhas[data_planilhas["Município"] == municipio_selecionado]
        st.dataframe(filtered_data)

if __name__ == "__main__":
    show_dashboard()
