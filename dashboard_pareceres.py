import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def load_data(sheet_name):
    return pd.read_excel('contPGT_contPlanilhas.xlsx', sheet_name=sheet_name)

def show_dashboard():
    st.header("Pareceres Conclusivos")
    df_pareceres = load_data(sheet_name='contPareceres')

    assentamentos = ['Todos'] + sorted(list(df_pareceres['Assentamento'].unique()))
    formatos = ['Todos'] + sorted(list(df_pareceres['Formato'].unique()))
    andamentos = ['Todos'] + sorted(list(df_pareceres['Andamento'].unique()))

    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="parecer_assentamento")
    selected_formato = st.sidebar.selectbox("Selecione um formato:", formatos, key="parecer_formato")
    selected_andamento = st.sidebar.selectbox("Selecione um andamento:", andamentos, key="parecer_andamento")

    if selected_assentamento != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Assentamento'] == selected_assentamento]

    if selected_formato != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Formato'] == selected_formato]

    if selected_andamento != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Andamento'] == selected_andamento]

    pareceres_em_elaboracao = df_pareceres[df_pareceres['Andamento'] == 'Em elaboração'].shape[0]
    pareceres_concluidos = df_pareceres[df_pareceres['Andamento'] == 'Concluído'].shape[0]
    total_a_atingir = 5861

    fig_progress_pareceres = go.Figure()
    fig_progress_pareceres.add_trace(go.Bar(
        name='Em elaboração',
        x=['Pareceres'],
        y=[pareceres_em_elaboracao],
        marker_color='orange'
    ))
    fig_progress_pareceres.add_trace(go.Bar(
        name='Concluídos',
        x=['Pareceres'],
        y=[pareceres_concluidos],
        marker_color='green'
    ))
    fig_progress_pareceres.add_trace(go.Bar(
        name='Faltando',
        x=['Pareceres'],
        y=[max(0, total_a_atingir - (pareceres_em_elaboracao + pareceres_concluidos))],
        marker_color='lightgrey'
    ))
    fig_progress_pareceres.update_layout(
        barmode='stack',
        title='Progresso dos Pareceres',
        xaxis_title='Status',
        yaxis_title='Quantidade',
        legend_title='Legenda'
    )
    st.plotly_chart(fig_progress_pareceres)

    st.subheader("Gráfico de pizza - Assentamentos")
    assentamento_data = df_pareceres['Assentamento'].value_counts()
    fig_assentamento = px.pie(
        names=assentamento_data.index,
        values=assentamento_data.values,
        title='Distribuição dos Pareceres por Assentamento'
    )
    st.plotly_chart(fig_assentamento)

    st.subheader("Relação de pareceres")
    st.write(df_pareceres)

    st.subheader("Gráfico de barras - andamento")
    chart_data_andamento = df_pareceres['Andamento'].value_counts()
    st.bar_chart(chart_data_andamento)

    total_por_formato_andamento = df_pareceres.groupby(['Formato', 'Andamento']).size().reset_index(name='Quantidade de Pareceres')
    st.subheader("Quantidade de pareceres por formato e andamento")
    st.write(total_por_formato_andamento)
