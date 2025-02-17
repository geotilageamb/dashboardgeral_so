import streamlit as st
import pandas as pd
import plotly.express as px

# Função para remover caracteres especiais
def remove_special_chars(text):
    import unicodedata
    return ''.join(ch for ch in unicodedata.normalize('NFKD', text) if not unicodedata.combining(ch))

# Função para carregar os dados da planilha
@st.cache_data
def load_data():
    return pd.read_excel('03_contDocsRecebidos.xlsx')

def show_dashboard():
    st.header("Produto 2.2.1.1 da meta 2.2 Documentos recebidos de assentados e NMRFs")
    df_docs = load_data()

    # Remover caracteres especiais para facilitar a manipulação
    df_docs['Município'] = df_docs['Município'].apply(remove_special_chars)
    df_docs['Assentamento'] = df_docs['Assentamento'].apply(remove_special_chars)

    # Filtros para seleção
    municipios = ['Todos'] + sorted(df_docs['Município'].unique())
    assentamentos = ['Todos'] + sorted(df_docs['Assentamento'].unique())
    lotes = ['Todos'] + sorted(df_docs['Lote'].unique())

    selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio_docs")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento_docs")
    selected_lote = st.sidebar.selectbox("Selecione um lote:", lotes, key="lote_docs")

    # Aplicar filtros
    if selected_municipio != "Todos":
        df_docs = df_docs[df_docs['Município'] == selected_municipio]

    if selected_assentamento != "Todos":
        df_docs = df_docs[df_docs['Assentamento'] == selected_assentamento]

    if selected_lote != "Todos":
        df_docs = df_docs[df_docs['Lote'] == selected_lote]

    # Quadro total de arquivos por município e total geral
    st.subheader("Total de Arquivos por Município")
    total_por_municipio = df_docs['Município'].value_counts().reset_index()
    total_por_municipio.columns = ['Município', 'Quantidade de Arquivos']
    st.write(total_por_municipio)

    total_geral = df_docs.shape[0]
    st.write(f"**Total Geral de Arquivos: {total_geral}**")

    # Gráfico de pizza para distribuição de arquivos por município
    st.subheader("Distribuição de Arquivos por Município")
    fig_municipio = px.pie(df_docs, names='Município', title='Distribuição por Município')
    st.plotly_chart(fig_municipio)

    # Gráfico de pizza para distribuição de arquivos por assentamento
    st.subheader("Distribuição de Arquivos por Assentamento")
    fig_assentamento = px.pie(df_docs, names='Assentamento', title='Distribuição por Assentamento')
    st.plotly_chart(fig_assentamento)

    # Relação geral de documentos
    st.subheader("Relação Geral de Documentos")
    st.write(df_docs)

if __name__ == "__main__":
    show_dashboard()
