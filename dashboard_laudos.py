import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import unicodedata

@st.cache
def load_data(sheet_name):
    return pd.read_excel('contPGT_contPlanilhas.xlsx', sheet_name=sheet_name)

def remove_special_chars(text):
    return ''.join(ch for ch in unicodedata.normalize('NFKD', text) if not unicodedata.combining(ch))

def show_dashboard():
    st.header("Laudos de Supervisão Ocupacional")
    df_laudos = load_data(sheet_name='contLaudos')

    tecnicos = ['Todos'] + sorted(list(df_laudos['Técnico'].unique()))
    assentamentos = ['Todos'] + sorted(list(df_laudos['Assentamento'].unique()))
    tipos_de_laudo = ['Todos'] + sorted(list(df_laudos['Tipo de Laudo'].unique()))
    municipios = ['Todos'] + sorted(list(df_laudos['Município'].apply(remove_special_chars).unique()))
    modalidade = ['Todos'] + sorted(list(df_laudos['Modalidade'].unique()))

    start_date = datetime(2022, 1, 1).date()
    end_date = datetime.now().date()

    selected_tecnico = st.sidebar.selectbox("Selecione um técnico:", tecnicos, key="tecnico_laudos")
    selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio_laudos")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento_laudos")
    selected_tipo_laudo = st.sidebar.selectbox("Selecione um tipo de laudo:", tipos_de_laudo, key="tipo_laudo_laudos")
    selected_modalidade = st.sidebar.selectbox("Selecione uma modalidade:", modalidade, key="modalidade_laudos")

    if selected_tecnico != "Todos":
        df_laudos = df_laudos[df_laudos['Técnico'] == selected_tecnico]

    if selected_municipio != "Todos":
        df_laudos = df_laudos[df_laudos['Município'].apply(remove_special_chars) == remove_special_chars(selected_municipio)]

    if selected_assentamento != "Todos":
        df_laudos = df_laudos[df_laudos['Assentamento'] == selected_assentamento]

    if selected_tipo_laudo != "Todos":
        df_laudos = df_laudos[df_laudos['Tipo de Laudo'] == selected_tipo_laudo]

    if selected_modalidade != "Todos":
        df_laudos = df_laudos[df_laudos['Modalidade'] == selected_modalidade]

    start_date = st.sidebar.date_input("Data inicial:", start_date, key="start_date_laudos")
    end_date = st.sidebar.date_input("Data final:", end_date, key="end_date_laudos")
    df_laudos['Data'] = pd.to_datetime(df_laudos['Data'], format='%d/%m/%Y').dt.date
    df_laudos = df_laudos[(df_laudos['Data'] >= start_date) & (df_laudos['Data'] <= end_date)]

    st.subheader("Relação geral de laudos")
    st.write(df_laudos)

    st.subheader("Distribuição de laudos por tipo")
    chart_data = df_laudos['Tipo de Laudo'].value_counts()
    st.bar_chart(chart_data)

    st.subheader("Distribuição de laudos por tipo")
    pie_chart_data = df_laudos['Tipo de Laudo'].value_counts()
    fig = px.pie(names=pie_chart_data.index, values=pie_chart_data.values)
    st.plotly_chart(fig)

    total_por_tipo_laudo = df_laudos['Tipo de Laudo'].value_counts()
    total_de_laudos = total_por_tipo_laudo.sum()
    total_por_tipo_laudo = total_por_tipo_laudo.reset_index()
    total_por_tipo_laudo.columns = ['Tipo de Laudo', 'Quantidade de Laudos']
    total_por_tipo_laudo.loc[len(total_por_tipo_laudo)] = ['Total', total_de_laudos]

    st.subheader("Quantidade de laudos por tipo")
    st.write(total_por_tipo_laudo)

    st.subheader("Progresso dos Laudos de Vistoria")
    laudos_vistoria_atual = df_laudos[df_laudos['Modalidade'] == 'VISTORIA IN LOCO'].shape[0]
    total_vistoria_a_atingir = 4739

    fig_progress_vistoria = go.Figure()
    fig_progress_vistoria.add_trace(go.Bar(
        name='Concluídos',
        x=['Laudos de Vistoria'],
        y=[laudos_vistoria_atual],
        marker_color='green'
    ))
    fig_progress_vistoria.add_trace(go.Bar(
        name='Faltando',
        x=['Laudos de Vistoria'],
        y=[max(0, total_vistoria_a_atingir - laudos_vistoria_atual)],
        marker_color='lightgrey'
    ))
    fig_progress_vistoria.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Número de Laudos',
        yaxis=dict(range=[0, total_vistoria_a_atingir])
    )
    st.plotly_chart(fig_progress_vistoria)

    st.subheader("Progresso dos Laudos de Mutirão")
    laudos_mutirao_atual = df_laudos[df_laudos['Modalidade'] == 'MUTIRÃO'].shape[0]
    total_mutirao_a_atingir = 2746

    fig_progress_mutirao = go.Figure()
    fig_progress_mutirao.add_trace(go.Bar(
        name='Concluídos',
        x=['Laudos de Mutirão'],
        y=[laudos_mutirao_atual],
        marker_color='green'
    ))
    fig_progress_mutirao.add_trace(go.Bar(
        name='Faltando',
        x=['Laudos de Mutirão'],
        y=[max(0, total_mutirao_a_atingir - laudos_mutirao_atual)],
        marker_color='lightgrey'
    ))
    fig_progress_mutirao.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Número de Laudos',
        yaxis=dict(range=[0, total_mutirao_a_atingir])
    )
    st.plotly_chart(fig_progress_mutirao)
