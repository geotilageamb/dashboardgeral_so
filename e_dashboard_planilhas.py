import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_excel('05_contPlanilhas.xlsx')

def show_dashboard():
    st.header("Monitoramento de Planilhas por Assentamento")
    data_planilhas = load_data()

    st.header("Totais")
    total_assentamentos = len(data_planilhas)
    total_com_planilha = len(data_planilhas[data_planilhas["Planilha de monitoramento"] == "Sim"])

    totais_df = pd.DataFrame({
        "Total de Assentamentos": [total_assentamentos],
        "Total com Planilha de Monitoramento": [total_com_planilha]
    })
    st.table(totais_df)

    st.header("Distribuição por Município")
    municipios_count = data_planilhas["Município"].value_counts()
    st.bar_chart(municipios_count)

    st.header("Tabela Completa")
    st.dataframe(data_planilhas)

    # Opcional: Adicionar um filtro por município
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
