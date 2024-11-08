import streamlit as st
import pandas as pd

@st.cache
def load_data(sheet_name):
    return pd.read_excel('contPGT_contPlanilhas.xlsx', sheet_name=sheet_name)

def show_dashboard():
    st.header("Planilhas de monitoramento")
    data_planilhas = load_data(sheet_name='contPlanilhas')

    st.header("Totais")
    total_planilhas = len(data_planilhas)
    total_abas = data_planilhas["Quantidade de Abas"].sum()
    totais_df = pd.DataFrame({
        "Total de Planilhas": [total_planilhas],
        "Total de Abas": [total_abas]
    })
    st.table(totais_df)

    st.header("Tabela Completa")
    st.dataframe(data_planilhas)

    st.header("Distribuição de Abas por Planilha")
    st.bar_chart(data_planilhas.set_index("Nome da Planilha")["Quantidade de Abas"])
