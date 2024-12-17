import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import unicodedata

def show_dashboard():
    # Função para remover caracteres especiais e normalizar texto
    def remove_special_chars(text):
        if not isinstance(text, str):
            return text  # Retorna o valor original se não for uma string
        return ''.join(ch for ch in unicodedata.normalize('NFKD', text) if not unicodedata.combining(ch))

    # Carregar os dados do Excel
    file_path = "01_laudos_SO_infos.xlsx"
    df = pd.read_excel(file_path)

    # Preencher valores vazios na coluna 'Modalidade' com 'Desconhecido'
    df['Modalidade'] = df['Modalidade'].fillna('Desconhecido')

    # Preencher valores nulos na coluna 'Município' com 'Desconhecido'
    df['Município'] = df['Município'].fillna('Desconhecido')
    df['Município'] = df['Município'].apply(remove_special_chars)

    # Converter coluna de data
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

    # Definir título do aplicativo
    st.header("Laudos de Supervisão Ocupacional")

    # Calcular total de laudos por modalidade
    total_vistoria = len(df[df['Modalidade'] == 'VISTORIA IN LOCO'])
    total_mutirao = len(df[df['Modalidade'] == 'MUTIRÃO'])

    # Meta total para cada modalidade
    meta_vistoria = 4739
    meta_mutirao = 2746

    # Calcular percentuais
    percentual_vistoria = (total_vistoria / meta_vistoria) * 100
    percentual_mutirao = (total_mutirao / meta_mutirao) * 100

    # Exibir barras de progresso
    st.subheader("Progresso dos Laudos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Vistoria In Loco**")
        st.progress(min(percentual_vistoria/100, 1.0))
        st.write(f"{total_vistoria} de {meta_vistoria} laudos ({percentual_vistoria:.1f}%)")

    with col2:
        st.markdown("**Mutirão**")
        st.progress(min(percentual_mutirao/100, 1.0))
        st.write(f"{total_mutirao} de {meta_mutirao} laudos ({percentual_mutirao:.1f}%)")

    # Definir título da tabela com informações gerais sobre os laudos
    st.subheader("Relação de laudos")

    # Ordenar opções de pesquisa
    tecnicos = ['Todos'] + sorted(list(df['Técnico'].unique()))
    assentamentos = ['Todos'] + sorted(list(df['Assentamento'].unique()))
    tipos_de_laudo = ['Todos'] + sorted(list(df['Tipo de Laudo'].unique()))
    municipios = ['Todos'] + sorted(list(df['Município'].unique()))
    modalidade = ['Todos'] + sorted(list(df['Modalidade'].unique()))
    codigos_sipra = ['Todos'] + sorted(list(df['Código SIPRA'].unique()))

    # Data inicial padrão: 01/01/2022
    start_date = datetime(2022, 1, 1).date()

    # Data final padrão: dia atual
    end_date = datetime.now().date()

    # Filtros laterais
    selected_tecnico = st.sidebar.selectbox("Selecione um técnico:", tecnicos, key="tecnico")
    selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento")
    selected_tipo_laudo = st.sidebar.selectbox("Selecione um tipo de laudo:", tipos_de_laudo, key="tipo_laudo")
    selected_modalidade = st.sidebar.selectbox("Selecione uma modalidade:", modalidade, key="modalidade")
    selected_codigo_sipra = st.sidebar.selectbox("Selecione um Código SIPRA:", codigos_sipra, key="codigo_sipra")

    # Filtrar por técnico
    if selected_tecnico != "Todos":
        df = df[df['Técnico'] == selected_tecnico]

    # Filtrar por município
    if selected_municipio != "Todos":
        df = df[df['Município'] == selected_municipio]

    # Filtrar por assentamento
    if selected_assentamento != "Todos":
        df = df[df['Assentamento'] == selected_assentamento]

    # Filtrar por tipo de laudo
    if selected_tipo_laudo != "Todos":
        df = df[df['Tipo de Laudo'] == selected_tipo_laudo]

    # Filtrar por modalidade
    if selected_modalidade != "Todos":
        df = df[df['Modalidade'] == selected_modalidade]

    # Filtrar por Código SIPRA
    if selected_codigo_sipra != "Todos":
        df = df[df['Código SIPRA'] == selected_codigo_sipra]

    # Filtrar por data
    start_date = st.sidebar.date_input("Data inicial:", start_date, key="start_date")
    end_date = st.sidebar.date_input("Data final:", end_date, key="end_date")
    df = df[(df['Data'].dt.date >= start_date) & (df['Data'].dt.date <= end_date)]

    # Exibir tabela interativa
    st.write(df)

    # Gráfico de pizza - Distribuição por município
    st.subheader("Distribuição de Laudos por Município")
    municipio_data = df['Município'].value_counts()
    fig_municipio = px.pie(
        names=municipio_data.index,
        values=municipio_data.values,
        title='Distribuição dos Laudos por Município'
    )
    st.plotly_chart(fig_municipio)

    # Gráfico de barras por mês com seletor de ano
    st.subheader("Quantidade de Laudos por Mês")

    # Adicionar seletor de ano
    anos_disponiveis = sorted(df['Data'].dt.year.unique())
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('2022', key='btn_2022'):
            ano_selecionado = 2022
    with col2:
        if st.button('2023', key='btn_2023'):
            ano_selecionado = 2023
    with col3:
        if st.button('2024', key='btn_2024'):
            ano_selecionado = 2024

    # Definir ano padrão se nenhum botão foi pressionado
    if 'ano_selecionado' not in locals():
        ano_selecionado = datetime.now().year

    # Filtrar dados pelo ano selecionado
    df_ano = df[df['Data'].dt.year == ano_selecionado]

    # Criar gráfico de barras mensal
    laudos_por_mes = df_ano.groupby(df_ano['Data'].dt.month).size().reindex(range(1, 13), fill_value=0)

    # Converter números dos meses para nomes
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    laudos_por_mes.index = meses

    fig_mensal = px.bar(
        x=laudos_por_mes.index,
        y=laudos_por_mes.values,
        title=f'Quantidade de Laudos por Mês em {ano_selecionado}',
        labels={'x': 'Mês', 'y': 'Quantidade de Laudos'}
    )
    st.plotly_chart(fig_mensal)

    # Gráfico de barras - tipo de laudo
    st.subheader("Gráfico de barras - tipo de laudo")
    chart_data = df['Tipo de Laudo'].value_counts()
    st.bar_chart(chart_data)

    # Gráfico de pizza - tipo de laudo
    st.subheader("Gráfico de pizza - tipo de laudo")
    pie_chart_data = df['Tipo de Laudo'].value_counts()
    fig = px.pie(names=pie_chart_data.index, values=pie_chart_data.values, title='Distribuição dos Laudos')
    st.plotly_chart(fig)

    # Calcular o total de laudos para cada tipo de laudo
    total_por_tipo_laudo = df['Tipo de Laudo'].value_counts()

    # Calcular o total de laudos
    total_de_laudos = total_por_tipo_laudo.sum()

    # Adicionar o total de laudos ao DataFrame
    total_por_tipo_laudo = total_por_tipo_laudo.reset_index()
    total_por_tipo_laudo.columns = ['Tipo de Laudo', 'Quantidade de Laudos']
    total_por_tipo_laudo.loc[len(total_por_tipo_laudo)] = ['Total', total_de_laudos]

    # Exibir quadro com os totais
    st.subheader("Quantidade de laudos por tipo")
    st.write(total_por_tipo_laudo)

if __name__ == "__main__":
    show_dashboard()
