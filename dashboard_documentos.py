import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def load_data(sheet_name):
    return pd.read_excel('contPGT_contPlanilhas.xlsx', sheet_name=sheet_name)

def show_dashboard():
    st.header("Dashboard de Documentos PGT")
    df_pgt = load_data(sheet_name='contPGT')

    if 'Objetivo' in df_pgt.columns:
        df_pgt['Objetivo'].fillna('Não especificado', inplace=True)

    tipos_documento = ['Todos'] + sorted(list(df_pgt['Tipo de documento PGT'].unique()))
    assentamentos = ['Todos'] + sorted(list(df_pgt['Assentamento'].unique()))
    nomes_t1 = ['Todos'] + sorted(list(df_pgt['Nome T1'].unique()))

    if 'Objetivo' in df_pgt.columns:
        objetivos = ['Todos'] + sorted(list(df_pgt['Objetivo'].unique()))
    else:
        objetivos = ['Todos']

    selected_tipo_documento = st.sidebar.selectbox("Selecione um tipo de documento:", tipos_documento, key="tipo_documento_pgt")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento_pgt")
    selected_nome_t1 = st.sidebar.selectbox("Selecione um nome T1:", nomes_t1, key="nome_t1_pgt")
    selected_objetivo = st.sidebar.selectbox("Selecione um objetivo:", objetivos, key="objetivo_pgt")

    if selected_tipo_documento != "Todos":
        df_pgt = df_pgt[df_pgt['Tipo de documento PGT'] == selected_tipo_documento]

    if selected_assentamento != "Todos":
        df_pgt = df_pgt[df_pgt['Assentamento'] == selected_assentamento]

    if selected_nome_t1 != "Todos":
        df_pgt = df_pgt[df_pgt['Nome T1'] == selected_nome_t1]

    if selected_objetivo != "Todos" and 'Objetivo' in df_pgt.columns:
        df_pgt = df_pgt[df_pgt['Objetivo'] == selected_objetivo]

    st.markdown("### Distribuição dos documentos por tipo")
    tipo_documento_data = df_pgt['Tipo de documento PGT'].value_counts()
    fig_tipo_documento = px.pie(
        names=tipo_documento_data.index,
        values=tipo_documento_data.values,
    )
    st.plotly_chart(fig_tipo_documento)

    st.markdown("### Distribuição dos documentos por assentamento")
    assentamento_data = df_pgt['Assentamento'].value_counts()
    st.bar_chart(assentamento_data)

    if 'Objetivo' in df_pgt.columns:
        st.markdown("### Distribuição dos documentos por objetivo")
        objetivo_data = df_pgt['Objetivo'].value_counts()
        st.bar_chart(objetivo_data)

    st.markdown("### Relação geral da documentação")
    st.write(df_pgt)

    total_por_tipo_assentamento = df_pgt.groupby(['Tipo de documento PGT', 'Assentamento']).size().reset_index(name='Quantidade de Documentos')
    st.markdown("### Quantidade de documentos por tipo e assentamento")
    st.write(total_por_tipo_assentamento)

    st.markdown("### Progresso de solicitação de documentação complementar")
    solicitacoes_atual = df_pgt[df_pgt['Tipo de documento PGT'] == 'Solicitação de documentação complementar'].shape[0]
    total_a_atingir = 674

    fig_progress = go.Figure()
    fig_progress.add_trace(go.Bar(
        name='Concluídos',
        x=['Solicitações'],
        y=[solicitacoes_atual],
        marker_color='green'
    ))
    fig_progress.add_trace(go.Bar(
        name='A atingir',
        x=['Solicitações'],
        y=[max(0, total_a_atingir - solicitacoes_atual)],
        marker_color='lightgrey'
    ))
    fig_progress.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Número de Documentos',
        yaxis=dict(range=[0, total_a_atingir])
    )
    st.plotly_chart(fig_progress)
