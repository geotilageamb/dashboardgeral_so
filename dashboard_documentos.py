import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_excel('contPGT.xlsx')

def show_dashboard():
    st.header("Dashboard de Documentos PGT")
    df_pgt = load_data()

    if 'Objetivo' in df_pgt.columns:
        df_pgt['Objetivo'].fillna('Não especificado', inplace=True)

    if 'Município' not in df_pgt.columns:
        st.error("A coluna 'Município' não está presente nos dados.")
        return

    tipos_documento = ['Todos'] + sorted(list(df_pgt['Tipo de documento PGT'].unique()))
    assentamentos = ['Todos'] + sorted(list(df_pgt['Assentamento'].unique()))
    municipios = ['Todos'] + sorted(list(df_pgt['Município'].unique()))
    nomes_t1 = ['Todos'] + sorted(list(df_pgt['Nome T1'].unique()))

    if 'Objetivo' in df_pgt.columns:
        objetivos = ['Todos'] + sorted(list(df_pgt['Objetivo'].unique()))
    else:
        objetivos = ['Todos']

    selected_tipo_documento = st.sidebar.selectbox("Selecione um tipo de documento:", tipos_documento, key="tipo_documento_pgt_unique")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento_pgt_unique")
    selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio_pgt_unique")
    selected_nome_t1 = st.sidebar.selectbox("Selecione um nome T1:", nomes_t1, key="nome_t1_pgt_unique")
    selected_objetivo = st.sidebar.selectbox("Selecione um objetivo:", objetivos, key="objetivo_pgt_unique")

    # Aplicar filtros
    filtered_df = df_pgt.copy()
    if selected_tipo_documento != "Todos":
        filtered_df = filtered_df[filtered_df['Tipo de documento PGT'] == selected_tipo_documento]
    if selected_assentamento != "Todos":
        filtered_df = filtered_df[filtered_df['Assentamento'] == selected_assentamento]
    if selected_municipio != "Todos":
        filtered_df = filtered_df[filtered_df['Município'] == selected_municipio]
    if selected_nome_t1 != "Todos":
        filtered_df = filtered_df[filtered_df['Nome T1'] == selected_nome_t1]
    if selected_objetivo != "Todos" and 'Objetivo' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Objetivo'] == selected_objetivo]

    # Gráficos principais
    st.markdown("### Distribuição dos documentos por tipo")
    tipo_documento_data = filtered_df['Tipo de documento PGT'].value_counts()
    fig_tipo_documento = px.pie(
        names=tipo_documento_data.index,
        values=tipo_documento_data.values,
    )
    st.plotly_chart(fig_tipo_documento)

    st.markdown("### Distribuição dos documentos por assentamento")
    assentamento_data = filtered_df['Assentamento'].value_counts()
    st.bar_chart(assentamento_data)

    st.markdown("### Distribuição dos documentos por município")
    municipio_data = filtered_df['Município'].value_counts()
    fig_municipio = px.pie(
        names=municipio_data.index,
        values=municipio_data.values,
    )
    st.plotly_chart(fig_municipio)

    if 'Objetivo' in filtered_df.columns:
        st.markdown("### Distribuição dos documentos por objetivo")
        objetivo_data = filtered_df['Objetivo'].value_counts()
        st.bar_chart(objetivo_data)

    # Barras de progresso
    st.markdown("### Progresso de Documentação")

    # Progresso de solicitação de documentação complementar
    st.subheader("Solicitação de documentação complementar")
    solicitacoes_atual = df_pgt[df_pgt['Tipo de documento PGT'] == 'Solicitação de documentação complementar'].shape[0]
    total_solicitacoes = 674

    fig_progress_sol = go.Figure()
    fig_progress_sol.add_trace(go.Bar(
        name='Concluídos',
        x=['Solicitações'],
        y=[solicitacoes_atual],
        marker_color='green'
    ))
    fig_progress_sol.add_trace(go.Bar(
        name='A atingir',
        x=['Solicitações'],
        y=[max(0, total_solicitacoes - solicitacoes_atual)],
        marker_color='lightgrey'
    ))
    fig_progress_sol.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Número de Documentos',
        yaxis=dict(range=[0, total_solicitacoes])
    )
    st.plotly_chart(fig_progress_sol)

    # Progresso dos segundos relatórios de conformidade
    st.subheader("Segundos Relatórios de Conformidade")
    segundos_relatorios_atual = df_pgt[df_pgt['Tipo de documento PGT'].str.contains('2º Relatório', na=False)].shape[0]
    total_segundos_relatorios = 337

    fig_progress_rel = go.Figure()
    fig_progress_rel.add_trace(go.Bar(
        name='Concluídos',
        x=['Segundos Relatórios'],
        y=[segundos_relatorios_atual],
        marker_color='blue'
    ))
    fig_progress_rel.add_trace(go.Bar(
        name='A atingir',
        x=['Segundos Relatórios'],
        y=[max(0, total_segundos_relatorios - segundos_relatorios_atual)],
        marker_color='lightgrey'
    ))
    fig_progress_rel.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Número de Documentos',
        yaxis=dict(range=[0, total_segundos_relatorios])
    )
    st.plotly_chart(fig_progress_rel)

    # Tabelas de dados
    st.markdown("### Relação geral da documentação")
    st.write(filtered_df)

    total_por_tipo_assentamento = filtered_df.groupby(['Tipo de documento PGT', 'Assentamento']).size().reset_index(name='Quantidade de Documentos')
    st.markdown("### Quantidade de documentos por tipo e assentamento")
    st.write(total_por_tipo_assentamento)

    # Métricas adicionais para segundos relatórios
    st.markdown("### Métricas de Segundos Relatórios")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total de Segundos Relatórios",
            segundos_relatorios_atual
        )

    with col2:
        st.metric(
            "Meta a Atingir",
            total_segundos_relatorios
        )

    with col3:
        percentual = round((segundos_relatorios_atual / total_segundos_relatorios) * 100, 2)
        st.metric(
            "Progresso (%)",
            f"{percentual}%"
        )

# Chamada para exibir o dashboard
show_dashboard()
