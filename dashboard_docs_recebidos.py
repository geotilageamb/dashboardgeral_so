import streamlit as st
import pandas as pd
import plotly.express as px

# Função para remover caracteres especiais
def remove_special_chars(text):
    import unicodedata
    return ''.join(ch for ch in unicodedata.normalize('NFKD', text) if not unicodedata.combining(ch))

# Função para carregar os dados da planilha gerada
@st.cache
def load_data(sheet_name):
    return pd.read_excel('contPGT_contPlanilhas.xlsx', sheet_name=sheet_name)

def show_dashboard():
    st.header("Dashboard de Documentos Recebidos")
    df_docs = load_data(sheet_name='contDocsRecebidos')  # Substitua 'NomeDaAba' pelo nome real da quinta aba

    municipios = ['Todos'] + sorted(list(df_docs['Município'].apply(remove_special_chars).unique()))
    assentamentos = ['Todos'] + sorted(list(df_docs['Assentamento'].unique()))
    lotes = ['Todos'] + sorted(list(df_docs['Lote'].unique()))

    selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio_docs")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento_docs")
    selected_lote = st.sidebar.selectbox("Selecione um lote:", lotes, key="lote_docs")

    if selected_municipio != "Todos":
        df_docs = df_docs[df_docs['Município'].apply(remove_special_chars) == remove_special_chars(selected_municipio)]

    if selected_assentamento != "Todos":
        df_docs = df_docs[df_docs['Assentamento'] == selected_assentamento]

    if selected_lote != "Todos":
        df_docs = df_docs[df_docs['Lote'] == selected_lote]

    st.subheader("Relação geral de documentos")
    st.write(df_docs)

    st.subheader("Distribuição de documentos por município")
    chart_data = df_docs['Município'].value_counts()
    st.bar_chart(chart_data)

    st.subheader("Distribuição de documentos por assentamento")
    pie_chart_data = df_docs['Assentamento'].value_counts()
    fig = px.pie(names=pie_chart_data.index, values=pie_chart_data.values)
    st.plotly_chart(fig)

    st.subheader("Quantidade de documentos por lote")
    total_por_lote = df_docs['Lote'].value_counts().reset_index()
    total_por_lote.columns = ['Lote', 'Quantidade de Documentos']
    st.write(total_por_lote)
